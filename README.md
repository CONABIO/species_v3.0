# species_v3.0

On this repository you will find the Beta version of SPECIES (Plataforma de exploración de datos ecológicos). On this Beta version, the team tries to explore a new database structure in order to facilitate and expand the type of data that can SPECIES worked with, seeking not only to accept biotic data but also data from different sources. 

The following ER Diagram is the first draft to explore and discuss main fields and relations among tables.

```mermaid
erDiagram
    cargaInformacionBase{
        string var1
        string var2
        string var3
        string varN
    }
    rel_occgeo_geomalla }|--|{ occ_variable : contiene
    rel_occgeo_geomalla }|--|{ occ_malla : contiene
    rel_occgeo_geomalla{
        integer idocc
        integer idgeo-malla
    }
    occ_variable }|--|| fuente_datos : tiene
    occ_variable{
        integer idocc_var
        integer idfuente_dato
        jsonb metadatos
    }
    fuente_datos{
        serial idfuente_dato
        varchar fuente_datos
        json esquema_metadatos
        varchar tipo_dato
        boolean es_tercero
    }
    occ_malla }|--|| area : tiene
    occ_malla{
        serial idocc_malla
        geom the_geom
        integer idarea
    }
    area{
        serial idarea
        integer idregion
        string region
        string resolucion
        array gids
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
