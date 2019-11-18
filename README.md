# Overview
[![Build Status](https://travis-ci.org/ww-tech/lookml-tools.svg?branch=master)](https://travis-ci.org/ww-tech/lookml-tools)
[![PyPI pyversions](https://img.shields.io/pypi/pyversions/lookml-tools.svg)](https://pypi.python.org/pypi/lookml-tools/)
[![PyPI version](https://badge.fury.io/py/lookml-tools.svg)](https://badge.fury.io/py/lookml-tools)
[![PyPI license](https://img.shields.io/pypi/l/lookml-tools.svg)](https://pypi.python.org/pypi/lookml-tools/)
[![Docs status](https://img.shields.io/website/https/ww-tech.github.io/lookml-tools?down_color=red&down_message=docs&label=docs&up_color=success&up_message=up)](https://ww-tech.github.io/lookml-tools/)


![](img/lookmltools.png)

# LookML Tools

This repository contains some tools to handle best practices of a set of developers working on LookML files. The tools in this repository have been adjusted specifically to run for Cimpress Looker projects.

Sites:
 - source: https://github.com/ww-tech/lookml-tools
 - documentation: https://ww-tech.github.io/lookml-tools/
 - Pypi: https://pypi.org/project/lookml-tools/

## LookML grapher
This tool creates a "network diagram" of the `model - explore - view` relationships and writes to an `PNG` image file. Additioanlly, the code will also:
 - identify any `orphans` i.e. views not referenced by any models or explores;
 - identify the inheritance relationships between views and explores;
 - build a connected graph of dependencies, when given root nodes, i.e., show all Looker objects where the given views and explores are used.

Full original documentation is [here](README_GRAPHER.md).

## Installation

Clone this repository:
```
git clone https://github.com/Cimpress-MCP/lookml-tools.git
```

To run the grapher for any Looker project repository, you will need to install grapviz and other dependencies:
```
cd lookml-tools/
pip install -r requirements.txt
brew install graphviz
```

You will need to copy the repository of the Looker project into lookml-tools/config/grapher. For example, you can clone a git repository of your Looker project:
```
cd config/grapher
git clone https://.../my_looker_project.git
```

Run the grapher to build the "network diagram" of your Looker project and view the result:
```
python ../../run_grapher.py --config config_grapher.json
open graph.png
```

By default the full "network diagram" of the Looker project is constructed. This is configured in config_grapher.json file:
```
-- config_grapher.json

...
      "roots": ["*"]        
}
```

To build a connected subgraph based on the given root nodes, adjust the config_grapher.json file by including the names of the root views or explores, e.g.,

```
-- config_grapher.json

...
      "roots": ["root_view1.view", "root_view2.view"]        
}
```



