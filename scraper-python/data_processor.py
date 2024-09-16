import datetime
from typing import List, Dict
from scrapy.selector import Selector
import structlog
from text_utils import TextUtils

logger = structlog.get_logger()

def process_results(html_string: str, plan: str, provincia: str, localidad: str, especialidad: str, config_index: int) -> List[Dict[str, str]]:
    """
    Process the HTML results and extract provider information.

    Args:
        html_string (str): The HTML content of the search results page.
        plan (str): The healthcare plan.
        provincia (str): The province.
        localidad (str): The locality.
        especialidad (str): The medical specialty.
        config_index (int): The index of the current configuration.

    Returns:
        List[Dict[str, str]]: A list of dictionaries containing provider information.
    """
    selector = Selector(text=html_string)
    providers = selector.css('#listadoTabla > tbody > tr[class^="prestador"]')
    
    logger.debug("Number of providers found", count=len(providers))
    
    results = []
    provider_index = 1
    
    for provider in providers:
        try:
            name = TextUtils.clean_text(TextUtils.normalize_text(provider.css('.nombrePrestador::text').get(default='').strip()))
            
            if not name:
                logger.debug("Skipping empty provider")
                continue
            
            logger.debug("Extracting data for provider", name=name)
            
            consultorios = provider.xpath('.//following-sibling::tr[1]//tr[contains(@class, "prestadorConsultorioEspecialidad")]')
            
            for sub_index, consultorio in enumerate(consultorios, start=1):
                address = TextUtils.clean_text(TextUtils.normalize_text(consultorio.css('.direccionPrestador::text').get(default='').strip()))
                locality = TextUtils.clean_text(TextUtils.normalize_text(consultorio.css('.localidadPrestador::text').get(default='').strip()))
                phone = TextUtils.clean_text(TextUtils.normalize_text(consultorio.css('td:nth-of-type(2) div::text').get(default='').strip()))
                
                # Check for Consultorio Digital
                consultorio_digital = "True" if consultorio.css('img[alt="Atención virtual con un clic desde tu WhatsApp o mail"]').get() else "False"
                
                logger.debug("Provider details", 
                            provider_index=f"{provider_index}.{sub_index}",
                            name=name,
                            address=address,
                            locality=locality,
                            phone=phone,
                            consultorio_digital=consultorio_digital)
                
                results.append({
                    'config_index': config_index,
                    'indice': f"{provider_index}.{sub_index}",
                    'plan': plan,
                    'provincia': provincia,
                    'localidad': localidad,
                    'especialidad': especialidad,
                    'nombre': name,
                    'direccion': address,
                    'localidad_prestador': locality,
                    'telefono': phone,
                    'consultorio_digital': consultorio_digital,
                    'scraping_date': datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                })
            
            provider_index += 1
        except Exception as e:
            logger.error("Error processing provider", provider_index=provider_index, error=str(e))
    
    logger.info("Processed provider entries", count=len(results))
    return results