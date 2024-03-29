# Use case: Data Source Selection

The user will be able to select from a list, the data source that contains the elements required to run the analysis. The user must be informed of the coverage of each data source to make the appropriate selection. The data source selection should enable only the regions where there are occurrences of it.

```mermaid
flowchart LR
    User --> id1(Select data source)
    User --> id2(Get info of data source)
    id1 --> id3(Enable regions)
```