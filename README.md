# 🏍️ Catálogo Inteligente de Motocicletas

Aplicación web desarrollada en **Python** y **Streamlit** para la consulta, comparación y análisis de especificaciones técnicas de motocicletas.

El sistema fue diseñado como una herramienta de apoyo para asesores de ventas, permitiendo acceder de forma rápida a información técnica, material audiovisual y explicaciones de conceptos clave relacionados con el desempeño de una motocicleta. Su objetivo es facilitar la atención al cliente, reducir los tiempos de búsqueda de información y fortalecer el conocimiento del producto en el piso de venta.

## 🌟 Motivación

La idea surge a partir de la experiencia de formación de un asesor de experiencia al cliente, donde se identificaron dos desafíos principales:

* La necesidad de adaptarse rápidamente a una gran cantidad de información técnica.
* La importancia de transmitir seguridad y dominio del producto durante una asesoría comercial.

A partir de estas observaciones se desarrolló una plataforma capaz de centralizar información, facilitar comparaciones y proporcionar apoyo en la interpretación de conceptos técnicos, todo ello sin necesidad de instalar software adicional.

## 🎯 Objetivos

* Centralizar la información técnica de motocicletas.
* Facilitar la comparación entre modelos.
* Agilizar la atención al cliente.
* Reducir el tiempo de búsqueda de especificaciones.
* Servir como base para futuras herramientas de análisis y recomendación.

## 🚀 Funcionalidades

### Consulta de fichas técnicas

Acceso rápido a especificaciones técnicas organizadas de manera clara y estructurada.

### Comparador de motocicletas

Comparación textual y visual entre distintos modelos para identificar diferencias relevantes.

### Sistema de recomendación

Motor de recomendación basado en similitud entre motocicletas, permitiendo sugerir alternativas comparables.

### Material audiovisual

Integración de videos para complementar la presentación de los productos.

### Guía interactiva

Explicaciones accesibles sobre conceptos como:

* Potencia
* Caballos de fuerza (HP)
* Torque
* Revoluciones por minuto (RPM)
* Autonomía
* Cilindrada
* Relación peso-potencia

### Visualización estructurada del catálogo

Diferentes modos de navegación para facilitar la exploración del catálogo.

## 🏗️ Arquitectura

```text
                    Usuario
                        │
                        ▼
┌─────────────────────────────────────┐
│      PRESENTACIÓN (Streamlit)        │
│ Interfaz gráfica de la aplicación    │
└─────────────────────────────────────┘
                        │
                        ▼
┌─────────────────────────────────────┐
│        LÓGICA DE NEGOCIO            │
│ • Consulta de fichas técnicas       │
│ • Comparador de motocicletas        │
│ • Sistema de recomendación          │
│ • Guía interactiva para el asesor   │
└─────────────────────────────────────┘
                        │
                        ▼
┌─────────────────────────────────────┐
│   PROCESAMIENTO DE DATOS            │
│ Pandas • NumPy • scikit-learn       │
└─────────────────────────────────────┘
                        │
                        ▼
┌─────────────────────────────────────┐
│       ALMACENAMIENTO                │
│ CSV • Imágenes • Videos             │
└─────────────────────────────────────┘
```

## 🛠️ Tecnologías utilizadas

* Python
* Streamlit
* Pandas
* NumPy
* scikit-learn
* HTML/CSS (integrado en Streamlit)
* Streamlit Community Cloud

## 📈 Roadmap

### Integración de nuevas categorías de productos

La arquitectura modular del sistema permite reutilizar la plataforma con diferentes bases de datos, facilitando la incorporación de categorías como:

* Colchones
* Telefonía
* Línea blanca
* Electrónica
* Otras mercancías especializadas

### Integración con datos de ventas

Posibilidad de conectar la plataforma con información histórica de ventas para generar análisis estadísticos y detectar tendencias comerciales.

### Inventario en tiempo real

Integración con sistemas de inventario para consultar disponibilidad de productos por sucursal.

### Aplicación móvil

Migración futura hacia Android e iOS para facilitar el acceso desde el piso de venta.

## 💡 Filosofía del proyecto

Este proyecto no busca ser únicamente una demostración de capacidades técnicas. Su propósito principal es resolver un problema real mediante una herramienta accesible, intuitiva y fácil de utilizar.

La plataforma fue concebida bajo una idea sencilla:

> Proporcionar a cualquier asesor acceso inmediato al conocimiento del producto mediante una única liga web, sin instalaciones ni configuraciones adicionales.

## 🔗 Demo

Disponible en:

[Catálogo Inteligente de Motocicletas](https://sub-motos-publico-jn3uftpwcduj6ustm6vu6t.streamlit.app/)

## 👨‍💻 Autor

**Giovanni Jefté Aguilar Carmona**

Físico egresado de la Universidad Nacional Autónoma de México (UNAM), con interés en ciencia de datos, sistemas complejos, desarrollo de software y aplicaciones orientadas a la resolución de problemas reales.
