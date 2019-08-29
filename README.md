# MegaBack

A Code challenge service for managing solar plants

### Endpoints
- /plants
    - GET:
        - Retrieves all the Plants in database
        - Response: ```
{
    "plants": [
        {
            "id": 1,
            "name": "Test Plant"
        },
        {
            "id": 3,
            "name": "Test rest"
        }
    ]
}```
    - POST:
        - Creates a new Plant
        - Form:
            - name: required name of the plant
        - Response: ```
{
    "id": 4,
    "name": "created plant",
    "datapoints": []
}```
- /plant/<panel_id>
    - GET:
        - Retrieves a Plant based on their ID
        - Response: ```
{
    "id": 4,
    "name": "created plant",
    "datapoints": []
}```
    - PUT:
        - Updates a Plant based on their ID
        - Form:
            - name: required new name of the plant
        - Response: ```
{
    "id": 4,
    "name": "created plant",
    "datapoints": []
}```
    - DELETE:
        - Deletes a Plant based on their ID
        - Response: ```
{
    "deleted": true
}```
- /panels/refresh/<plant_id>
    - GET:
        - Performs a request to the Monitoring service and store the results in database if do not exists already
        - Response:```{
  "datapoints": [
    {
      "id": 73,
      "plant_id": 1,
      "expected": {
        "energy": 62.815189106221666,
        "irradiation": 18.557018909139796
      },
      "observed": {
        "energy": 5.692499240015888,
        "irradiation": 96.17545284370519
      },
      "datetime": "2019-01-01T00:00:00+01:00"
    },
    {
      "id": 74,
      "plant_id": 1,
      "expected": {
        "energy": 36.61909075253701,
        "irradiation": 30.38131890700517
      },
      "observed": {
        "energy": 9.341619767365922,
        "irradiation": 90.94176000202788
      },
      "datetime": "2019-01-01T01:00:00+01:00"
    }
  ]
} ```
- /panels/report:
    - TODO: Work in progress
