DEFAULT_CONFIG = {
    "git": {
        "url": "https://github.com/exampleorg/examplerepo.git",
        "folder": "gitrepo",
    },
    "grapher": {
        "output": "graph.png",
        "options": {
            "node_size": 500,
            "label_font_size": 18,
            "text_angle": 30,
            "image_width": 24,
            "image_height": 16,
        },
        "roots": ["*"],
    },
    "infile_globs": ["*.*.lkml", "**/*.*.lkml"],
    "linter": {
        "rules": {
            "file_level_rules": [
                {"name": "DataSourceRule", "run": True},
                {"name": "OneViewPerFileRule", "run": True},
                {"name": "FilenameViewnameMatchRule", "run": True},
            ],
            "field_level_rules": [
                {"name": "DescriptionRule", "run": True},
                {"name": "DrillDownRule", "run": True},
                {"name": "YesNoNameRule", "run": True},
                {"name": "CountNameRule", "run": True},
                {"name": "AllCapsRule", "run": True},
                {
                    "name": "LexiconRule",
                    "run": True,
                    "phrases": ["Subscriber", "Subscription", "studio"],
                },
            ],
            "other_rules": [{"name": "NoOrphansRule", "run": True}],
        },
        "output": {
            "csv": {
                "file_output": "linter_file_report.csv",
                "field_output": "linter_field_report.csv",
            },
            "bigquery": {
                "target_bucket_name": "your_bucket",
                "bucket_folder": "your_folder",
                "project_id": "your-project",
                "dataset": "your-dataset",
                "file_destination_table": "lookml_linter_file_report",
                "field_destination_table": "lookml_linter_field_report",
            },
        },
    },
    "updater": {
        "definitions": {"type": "CsvDefinitionsProvider", "filename": "definitions.csv"}
    },
}


class LazyConfig:
    def __init__(self):
        self._config = DEFAULT_CONFIG

    def __getitem__(self, key):
        return self._config.get(key)

    def __setitem__(self, key, val):
        self._config[key] = val

    def __contains__(self, item):
        return item in self._config


config = LazyConfig()
