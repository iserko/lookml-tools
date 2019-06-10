import os
import json
import pytest
from lkmltools.grapher.lookml_grapher import LookMlGrapher, NodeType
import networkx as nx

@pytest.fixture()
def config():
    config = {
        "parser": "lookml-parser",
        "infile_globs": ["test/grapher_lkml/*.lkml"],
        "tmp_file": "parsed_lookml.json",
        "output": "test/graph.png",
        "options": {
          "node_size": 500,
          "label_font_size": 18,
          "text_angle": 30,
          "image_width": 24,
          "image_height" : 16
        }
    }
    return config

def test_create_graph(config):
    grapher = LookMlGrapher(config)
    grapher.node_map['model_a'] = NodeType.MODEL
    grapher.node_map['explore_a'] = NodeType.EXPLORE
    grapher.node_map['view_a'] = NodeType.VIEW
    grapher.models_to_explores.append(('model_a', 'explore_a'))
    grapher.explores_to_views.append(('explore_a','view_a'))
    g = grapher.create_graph()
    assert isinstance(g, nx.DiGraph)
    assert len(g) == 3

def test_orphans(config):
    grapher = LookMlGrapher(config)
    grapher.node_map['model_a'] = NodeType.MODEL
    grapher.node_map['explore_a'] = NodeType.EXPLORE
    grapher.node_map['view_a'] = NodeType.VIEW
    grapher.node_map['orphan'] = NodeType.VIEW
    grapher.models_to_explores.append(('model_a', 'explore_a'))
    grapher.explores_to_views.append(('explore_a','view_a'))
    grapher.tag_orphans()
    orphans = grapher.orphans()
    assert len(orphans) == 1
    assert list(orphans)[0] == 'orphan'

def test_plot_graph(config):
    img_file = config['output']
    if os.path.exists(config['output']):
        os.remove(img_file)

    grapher = LookMlGrapher(config)
    grapher.node_map['model_a'] = NodeType.MODEL
    grapher.node_map['explore_a'] = NodeType.EXPLORE
    grapher.node_map['view_a'] = NodeType.VIEW
    grapher.node_map['orphan'] = NodeType.VIEW
    grapher.models_to_explores.append(('model_a', 'explore_a'))
    grapher.explores_to_views.append(('explore_a','view_a'))
    grapher.tag_orphans()
    g = grapher.create_graph()

    grapher.plot_graph(g, img_file, "some title")

    assert os.path.exists(img_file)

    if os.path.exists(config['output']):
        os.remove(img_file)

def test_process_explores(config):
    grapher = LookMlGrapher(config)
    json_data = grapher.lookml.get_json_representation("test/grapher_lkml/some_model.model.lkml")

    m = json_data['files'][0]['models'][0]
    e = m['explores'][0]

    assert grapher.models_to_explores == []
    assert grapher.explores_to_views == []

    grapher.process_explores(m, e)

    assert grapher.models_to_explores == [('some_model','some_explore')]
    assert grapher.explores_to_views == [('some_explore','some_view'), ('some_explore','some_other_view')]

    if os.path.exists(config['tmp_file']):
        os.remove(config['tmp_file'])

def test_process_file(config):
    grapher = LookMlGrapher(config)
    assert grapher.models_to_explores == []
    assert grapher.explores_to_views == []
    grapher.process_file("test/grapher_lkml/some_model.model.lkml")
    assert grapher.models_to_explores == [('some_model','some_explore')]
    assert grapher.explores_to_views == [('some_explore','some_view'), ('some_explore','some_other_view')]
    if os.path.exists(config['tmp_file']):
        os.remove(config['tmp_file'])

def test_process_file2(config):
    grapher = LookMlGrapher(config)
    assert grapher.models_to_explores == []
    assert grapher.explores_to_views == []

    json_data = grapher.lookml.get_json_representation("test/grapher_lkml/some_model.model.lkml")
    grapher.process_file(None, json_data)

    assert grapher.models_to_explores == [('some_model','some_explore')]
    assert grapher.explores_to_views == [('some_explore','some_view'), ('some_explore','some_other_view')]
    if os.path.exists(config['tmp_file']):
        os.remove(config['tmp_file'])

def test_process_file3(config):
    grapher = LookMlGrapher(config)
    assert grapher.node_map == {}
    grapher.process_file("test/grapher_lkml/some_view.view.lkml")

    assert 'some_view' in grapher.node_map
    assert grapher.node_map['some_view'] == NodeType.VIEW
    if os.path.exists(config['tmp_file']):
        os.remove(config['tmp_file'])

def test_process_file4(config):
    grapher = LookMlGrapher(config)
    assert grapher.models_to_explores == []
    assert grapher.explores_to_views == []
    grapher.process_file("test/grapher_lkml/some_explore.exlore.lkml")
    assert grapher.models_to_explores == []
    assert grapher.explores_to_views == [('some_explore','some_view'), ('some_explore','some_other_view')]
    if os.path.exists(config['tmp_file']):
        os.remove(config['tmp_file'])

def test_process_file5(config):
    grapher = LookMlGrapher(config)
    with pytest.raises(Exception) as e:
        grapher.process_file("test/empty.view.lkml")
    assert 'No models, views, or explores?' in str(e.value)

def test_extract_graph_info(config):
    grapher = LookMlGrapher(config)
    assert grapher.node_map == {}
    assert grapher.models_to_explores == []
    assert grapher.explores_to_views == []
    grapher.extract_graph_info(["test/grapher_lkml/some_model.model.lkml"])
    assert grapher.models_to_explores == [('some_model','some_explore')]
    assert grapher.explores_to_views == [('some_explore','some_view'), ('some_explore','some_other_view')]
    assert len(grapher.node_map) == 2
    assert 'some_explore' in grapher.node_map
    assert grapher.node_map['some_explore'] == NodeType.EXPLORE
    assert 'some_model' in grapher.node_map
    assert grapher.node_map['some_model'] == NodeType.MODEL
    if os.path.exists(config['tmp_file']):
        os.remove(config['tmp_file'])

def test_run(config):
    grapher = LookMlGrapher(config)

    img_file = config['output']
    if os.path.exists(config['output']):
        os.remove(img_file)

    grapher.run()

    assert os.path.exists(img_file)

    if os.path.exists(config['output']):
        os.remove(img_file)
    if os.path.exists(config['tmp_file']):
        os.remove(config['tmp_file'])
