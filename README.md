# species_v3.0

On this repository you will find the Beta version of SPECIES (Plataforma de exploración de datos ecológicos). On this Beta version, the team tries to explore a new database structure in order to facilitate and expand the type of data that can SPECIES worked with, seeking not only to accept biotic data but also data from different sources. 

The following ER Diagram is the first draft to explore and discuss main fields and relations amoung tables.

```mermaid
erDiagram
    cargaInformacionBase{
        string var1
        string var2
        string var3
        string varN
    }
    rel_occgeo_geomalla }|--|{ occ_geo : contiene
    rel_occgeo_geomalla }|--|{ geo_malla : contiene
    rel_occgeo_geomalla{
        integer idocc
        integer idgeo-malla
    }
    occ_geo }|--|| fuente_datos : tiene
    occ_geo{
        serial idocc
        geom the_geom
        int idfuente_dato
        json metadatos
    }
    fuente_datos{
        serial idfuente_dato
        string fuente_datos
        json scheme_metadatos
        string tipo_dato
        boolean tercero
    }
    geo_malla }|--|| region : tiene
    geo_malla{
        serial idgeo_malla
        geom the_geom
        integer idregion
    }
    region{
        integer idregion
        string region
        array gids
        string descripcion
        string resolucion
    }
    historicos_analisis{
        integer idhistorico
        string nombre
        string configuracion
        time duracion
        timestamp tsolicitud
        timestamp trespuesta
        string origen
    }
    sessions{
        serial sid
        string sess
        time expire
    }
    analisis_nodos{
        serial idnanalisis
        string resultado
    }
    usuarios_species{
       serial idusuario
       string nombre
       string correo
       string contrasenia
       boolean acepta_terminos
       string procedencia
       timestamp fecha_registro 
    }
```
