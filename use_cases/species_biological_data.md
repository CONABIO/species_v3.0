# Biological data - Use case

The user can perform ecological niche analysis through the selection of specific parameters. The user can select the data sources available on the platform, whether from the Sistema Nacional de Información Sobre la Biodiversidad (SNIB) or the Global Biodiversity Information Facility (GBIF). The user can select, depending on the data source, a geographical area to view the results, as well as the resolution to count the correlations that exist between our target group and the covariates.

The selection of the target group depends on the selected data source, where it is currently composed of biotic data. If required, they can be filtered by date range in which the occurrence was recorded, discard undated records and fossil records. This configuration can be previewed on a presence map and seen in detail at the selected resolution level.

For the selection of covariates, there is access to biotic and abiotic records. Abiotic data covers climatic records, topography and natural features. In addition, it is possible to configure cross-validation of the analysis, discard covariates by minimum number of occurrences and a priori analysis.

As a result of executing this niche analysis, we obtain the generation of different visual elements and tables. The tables show the results of the relationship that exists between our target group and the selected covariates through the epsilon and score correlation measures, see the article [here](https://onlinelibrary.wiley.com/doi/full/10.1002/ece3.4800). The visual elements consist of a map and histograms. On the map we can see the regions where the presence of our target group favors and the regions where the presence of the target group disfavors. In addition, you can see the details of the covariates that participate in the result of each selected cell. For histograms, we can observe the results grouped, either by epsilon or by score obtained, in deciles or average of occurrences ​​by ranges.

Most of the results of the tables and maps can be exported in csv formats or the georeferenced data in geojson format to be visualized in geographic information systems.


