// Importar las bibliotecas necesarias
const axios = require("axios");
const createCsvWriter = require("csv-writer").createObjectCsvWriter;

//Configuraciones de las URL de consulta para cada especialidad y provincia
const configurations = [
  {
    baseUrl:
      "https://www.osde.com.ar/Cartilla/consultaPorEspecialidadRemote.ashx?metodo=ObtenerParaCartillaMedica&rubros=2&rubroId=2&provinciaId=1&provinciaTipo=METRO&provinciaNombre=Ciudad%20de%20Buenos%20Aires&localidadId=0&localidadNombre=Todas%20las%20localidades&planId=51&planNombre=510&especialidadId=810&especialidadNombre=Psicolog%C3%ADa%20adultos&filialId=&hiddenLat=&hiddenLng=&textDireccion=&textNombre=&txtFecha=&ordenador=&hidDetalleNombre=&hidDetalleDireccion=&hidDetalleTelefono=&hidDetalleObservacion=&hidDetalleEspecialidad=&hidDetalleLatitud=&hidDetalleLongitud=&prestadoresEnLista=0&modalidadAtencion=2",
    plan: "510",
    provincia: "Ciudad de Buenos Aires",
    especialidad: "PSICOLOGÍA ADULTOS",
  },
  {
    baseUrl:
      "https://www.osde.com.ar/Cartilla/consultaPorEspecialidadRemote.ashx?metodo=ObtenerParaCartillaMedica&rubros=2&rubroId=2&provinciaId=1&provinciaTipo=METRO&provinciaNombre=Ciudad%20de%20Buenos%20Aires&localidadId=0&localidadNombre=Todas%20las%20localidades&planId=51&planNombre=510&especialidadId=870&especialidadNombre=Psicolog%C3%ADa%20ni%C3%B1os%20y%20adolescentes&filialId=60&hiddenLat=&hiddenLng=&textDireccion=&textNombre=&txtFecha=&ordenador=&hidDetalleNombre=&hidDetalleDireccion=&hidDetalleTelefono=&hidDetalleObservacion=&hidDetalleEspecialidad=&hidDetalleLatitud=&hidDetalleLongitud=&prestadoresEnLista=0&modalidadAtencion=2",
    plan: "510",
    provincia: "Ciudad de Buenos Aires",
    especialidad: "PSICOLOGÍA NIÑOS Y ADOLESCENTES",
  },
  {
    baseUrl:
      "https://www.osde.com.ar/Cartilla/consultaPorEspecialidadRemote.ashx?metodo=ObtenerParaCartillaMedica&rubros=2&rubroId=2&provinciaId=4&provinciaTipo=METRO&provinciaNombre=GBA%20Zona%20Oeste&localidadId=0&localidadNombre=Todas%20las%20localidades&planId=21&planNombre=210&especialidadId=810&especialidadNombre=Psicolog%C3%ADa%20adultos&filialId=60&hiddenLat=&hiddenLng=&textDireccion=&textNombre=&txtFecha=&ordenador=&hidDetalleNombre=&hidDetalleDireccion=&hidDetalleTelefono=&hidDetalleObservacion=&hidDetalleEspecialidad=&hidDetalleLatitud=&hidDetalleLongitud=&prestadoresEnLista=0&modalidadAtencion=2",
    plan: "210",
    provincia: "GBA Zona Oeste",
    especialidad: "PSICOLOGÍA ADULTOS",
  },
  {
    baseUrl:
      "https://www.osde.com.ar/Cartilla/consultaPorEspecialidadRemote.ashx?metodo=ObtenerParaCartillaMedica&rubros=2&rubroId=2&provinciaId=2&provinciaTipo=METRO&provinciaNombre=GBA%20Zona%20Norte&localidadId=0&localidadNombre=Todas%20las%20localidades&planId=21&planNombre=210&especialidadId=810&especialidadNombre=Psicolog%C3%ADa%20adultos&filialId=&hiddenLat=&hiddenLng=&textDireccion=&textNombre=&txtFecha=&ordenador=&hidDetalleNombre=&hidDetalleDireccion=&hidDetalleTelefono=&hidDetalleObservacion=&hidDetalleEspecialidad=&hidDetalleLatitud=&hidDetalleLongitud=&prestadoresEnLista=0&modalidadAtencion=2",
    plan: "210",
    provincia: "GBA Zona Norte",
    especialidad: "PSICOLOGÍA ADULTOS",
  },
];

// Configurar el escritor CSV
const csvWriter = createCsvWriter({
  path: "osde_professionals.csv",
  header: [
    { id: "configIndex", title: "ConfigIndex" },
    { id: "itemIndex", title: "IndiceItem" },
    { id: "nombre", title: "Nombre" },
    { id: "especialidad", title: "Especialidad" },
    { id: "direccion", title: "Dirección" },
    { id: "telefono", title: "Teléfono" },
    { id: "email", title: "Email" },
    { id: "localidad", title: "Localidad" },
    { id: "provincia", title: "Provincia" },
    { id: "plan", title: "Plan" },
    { id: "numeroPrestador", title: "Número de Prestador" },
  ],
});

// Función para obtener datos de una página específica
async function fetchDataForPage(config, page, configIndex, startIndex) {
  const url = `${config.baseUrl}&hidPagina=${page}`;
  try {
    // Realizamos la solicitud HTTP
    const response = await axios.get(url, {
      headers: {
        Cookie:
          "BIGipServerwww.osdebinario.com.ar=265070784.37663.0000; SitioWeb=b90...",
        "Cache-Control": "no-cache",
        "User-Agent": "PostmanRuntime/7.41.2",
        Accept: "*/*",
        "Accept-Encoding": "gzip, deflate, br",
        Connection: "keep-alive",
      },
    });

    if (response.data && response.data.ListaPrestador) {
      let currentMainIndex = startIndex;
      let professionalIndex = {};

      // Procesamos cada prestador 
        return response.data.ListaPrestador.flatMap((p) => {
        // Inicializar o resetear el índice para cada prestador
        if (!professionalIndex[p.numeroPrestador]) {
          professionalIndex[p.numeroPrestador] = {
            mainIndex: currentMainIndex,
            subIndex: 1,
          };
          currentMainIndex++;
        } else {
          professionalIndex[p.numeroPrestador].subIndex = 1;
        }

        // Mapeamos cada consultorio a un item en el CSV
        return p.consultorios.map((consultorio) => {
          const { mainIndex, subIndex } = professionalIndex[p.numeroPrestador];
          const item = {
            configIndex: configIndex,
            itemIndex: `${configIndex}.${mainIndex}.${subIndex}`,
            nombre: p.nombre || "N/A",
            especialidad: config.especialidad,
            direccion: consultorio.direccion || "N/A",
            telefono: consultorio.telefono || "N/A",
            email: (consultorio.email || "").trim(),
            localidad: consultorio.localidad || "N/A",
            provincia: consultorio.provincia || config.provincia,
            plan: config.plan,
            numeroPrestador: p.numeroPrestador || "N/A",
          };
          professionalIndex[p.numeroPrestador].subIndex++;
          return item;
        });
      });
    } else {
      return [];
    }
  } catch (error) {
    console.error(
      `Error fetching data for ${config.especialidad} in ${config.provincia}, page ${page}: ${error.message}`
    );
    return [];
  }
}

// Función para obtener todos los datos de una configuración
async function fetchAllData(config, configIndex) {
  let allData = [];
  let page = 1;
  let hasMoreData = true;
  let startIndex = 1;

  while (hasMoreData) {
    console.log(
      `Fetching page ${page} for ${config.especialidad} in ${config.provincia}...`
    );
    const data = await fetchDataForPage(config, page, configIndex, startIndex);
    if (data.length > 0) {
      allData = allData.concat(data);
      console.log(`Fetched ${data.length} records from page ${page}`);
      page++;
      // Actualizar el índice de inicio para la siguiente página
      startIndex =
        Math.max(
          ...data.map((item) => parseInt(item.itemIndex.split(".")[1]))
        ) + 1;
      await new Promise((resolve) => setTimeout(resolve, 1000)); // Limitar la tasa de solicitudes
    } else {
      hasMoreData = false;
    }
  }

  console.log(
    `Total records fetched for ${config.especialidad} in ${config.provincia}: ${allData.length}`
  );
  return allData;
}

// Función principal para manejar el proceso
async function main() {
  let allData = [];
  for (let i = 0; i < configurations.length; i++) {
    const config = configurations[i];
    console.log(
      `Starting fetch for ${config.especialidad} in ${config.provincia}...`
    );
    const data = await fetchAllData(config, i + 1);
    allData = allData.concat(data);
    await new Promise((resolve) => setTimeout(resolve, 2000)); // Limitar la tasa entre configuraciones
  }

  // Escribir los datos en el archivo CSV si se obtuvieron datos
  if (allData.length > 0) {
    await csvWriter.writeRecords(allData);
    console.log(
      `Data saved to osde_professionals.csv (${allData.length} total records)`
    );
  } else {
    console.log("No data was fetched. CSV file was not created.");
  }
}

// Ejecutar la función principal y manejar cualquier error
main().catch(console.error);
