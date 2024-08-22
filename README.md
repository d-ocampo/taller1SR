# Sistema de Recomendación - LastFM 1k

Este proyecto es una implementación de un sistema de recomendación utilizando datos de la plataforma LastFM 1k. El sistema está desarrollado utilizando Dash, con una interfaz de usuario que permite explorar y analizar las recomendaciones basadas en diferentes modelos.

## Estructura del Proyecto

### Directorios Principales
- **layouts**: Contiene los archivos relacionados con el diseño de las diferentes páginas del sistema.
- **lay**: Contiene scripts específicos relacionados con el análisis de riesgo.
- **script_inicial**: Incluye scripts de funciones auxiliares, como el cálculo del RMSE.

### Archivos Clave
- **app_.py**: Archivo principal que inicializa la aplicación y define la estructura de la interfaz de usuario.
- **spatial.py**: Contiene las funciones relacionadas con la visualización espacial de recomendaciones.
- **RMSE.py**: Script para calcular el RMSE de los modelos implementados.

## Requisitos

- Python 3.x
- Las siguientes bibliotecas de Python:
  - `dash`
  - `dash-bootstrap-components`
  - `dash-core-components`
  - `dash-html-components`
  - `plotly`
  - `networkx`
  - `pandas`

## Instalación

1. Clona este repositorio:
    ```bash
    git clone <URL_del_Repositorio>
    ```
2. Instala los requisitos:
    ```bash
    pip install -r requirements.txt
    ```

3. Ejecuta la aplicación:
    ```bash
    python app_.py
    ```

## Descripción de la Aplicación

### Barras de Navegación

- **Top Navbar**: Muestra el título de la aplicación y cambia dinámicamente según la página seleccionada.
- **Sidebar**: Permite navegar entre diferentes secciones como Home, Dashboard, Recomendación, Exploración, y About Us.

### Funcionalidades Principales

1. **Home**: Página de inicio de la aplicación.
2. **Dashboard**: Permite visualizar y comparar el rendimiento de diferentes modelos utilizando el RMSE.
3. **Recomendación**: Ofrece recomendaciones personalizadas basadas en usuarios o ítems, utilizando diferentes modelos como Cosine y Pearson.
4. **Exploración**: Muestra gráficos interactivos de las canciones y artistas más escuchados por un usuario, permitiendo explorar el comportamiento y preferencias del mismo.
5. **About Us**: Información sobre el equipo de desarrollo.

### Modelos de Recomendación

La aplicación implementa varios modelos de recomendación:

- **Modelos basados en el usuario** (Cosine y Pearson).
- **Modelos basados en el ítem** (Cosine y Pearson).

### Gráficos y Visualizaciones

La aplicación incluye visualizaciones interactivas que permiten al usuario explorar redes de recomendaciones, así como gráficos de barras y circulares para analizar preferencias.

## Contribución

Las contribuciones son bienvenidas. Si deseas contribuir, por favor sigue los siguientes pasos:

1. Haz un fork del repositorio.
2. Crea una nueva rama (`git checkout -b feature/AmazingFeature`).
3. Realiza los cambios necesarios y haz un commit (`git commit -m 'Add some AmazingFeature'`).
4. Sube tus cambios (`git push origin feature/AmazingFeature`).
5. Crea un nuevo Pull Request.
