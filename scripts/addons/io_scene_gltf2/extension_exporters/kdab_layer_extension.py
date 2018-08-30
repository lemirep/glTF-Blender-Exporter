
class KDABLayers:
    ext_meta = {
        'name': 'KDAB_Layers',
        'isDraft': False,
        'enable': False,
        'url': (
            'https://www.kdab.com'
        ),
    }

    KDAB_layers_extension_name = 'KDAB_Layers'

    def export(self, export_settings, glTF):
        # Mark extension as being used
        glTF['extensionsUsed'] = glTF.get('extensionsUsed', [])
        glTF['extensionsUsed'].append(self.KDAB_layers_extension_name)

        # Export per node layers
        filtered_objects = export_settings['filtered_objects']

        # Gather mapping between glTf nodes and their names
        name_to_glTF_index_map = {value['name']: idx for idx, value in enumerate(glTF['nodes'])}

        # Gather blender objects that have been positively filtered for export
        exported_obj_pairs = [
            (blender_obj, glTF['nodes'][name_to_glTF_index_map[blender_obj.name]])
            for blender_obj in filtered_objects
        ]

        layer_names = []

        # Add references to extension in filtered gltF nodes
        for blender_obj, glTF_node in exported_obj_pairs:
            if 'kdab' in blender_obj.keys() and 'layers' in blender_obj.kdab.keys():
                node_layer_names = [layer.name for layer in blender_obj.kdab.layers]
                if node_layer_names:
                    # Gather any layer names not contained in the global layers array
                    new_layer_names = [layer_name for layer_name in node_layer_names if layer_name not in layer_names]
                    # Add any new layer to global list of layers
                    layer_names.extend(new_layer_names)

                    # Create or extend extensions set and add KDAB extension entry on node
                    glTF_node['extensions'] = glTF_node.get('extensions', {})
                    glTF_node['extensions'][self.KDAB_layers_extension_name] = {}

                    # Reference obj layers by using index into global layers array
                    glTF_node['extensions'][self.KDAB_layers_extension_name]['layers'] = [layer_names.index(layer_name) for layer_name in node_layer_names]


        # Add KDAB_Layers into glTf extension object
        glTF['extensions'] = glTF.get('extensions', {})
        glTF['extensions'][self.KDAB_layers_extension_name] = {}
        glTF['extensions'][self.KDAB_layers_extension_name]['layers'] = layer_names
