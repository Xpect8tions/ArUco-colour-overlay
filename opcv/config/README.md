# ids_params.yaml

This is a yaml file that will be updated by [update_yaml_on_collage.py](../opcv/update_yaml_on_collage.py) and is to be read by any file that wishes to view and colour your `collage16.jpg` file.

The dictionaries are saved like this:

```python
{
    <aruco_id> : [<status>,[<x_position>,<y_position>]]
    <aruco_id> : [<status>,[<x_position>,<y_position>]]
    <aruco_id> : [<status>,[<x_position>,<y_position>]]
                .
                .
                .
}
```

when viewed in the yaml:

```yaml
{
    <aruco_id>:
    - <status>
    - - <x_position>
      - <y_position>
    <aruco_id>:
    - <status>
    - - <x_position>
      - <y_position>
    <aruco_id>:
    - <status>
    - - <x_position>
      - <y_position>
            .
            .
            .
}
```
