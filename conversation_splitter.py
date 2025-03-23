#!/usr/bin/env python3
"""
Script para dividir un archivo JSON de conversaciones de ChatGPT en archivos individuales.
Cada conversación se guarda como un archivo separado con la fecha y título como nombre.
"""

import json
import os
import argparse
from datetime import datetime


def process_conversations(input_file, output_dir="output", export_markdown=False):
    """
    Procesa el archivo JSON de entrada y divide las conversaciones en archivos separados.

    Args:
        input_file (str): Ruta al archivo JSON de entrada
        output_dir (str): Directorio donde se guardarán los archivos de salida
        export_markdown (bool): Si es True, también exporta las conversaciones en formato Markdown
    """
    # Crear directorio de salida si no existe
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # Leer el archivo JSON
    with open(input_file, 'r', encoding='utf-8') as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError as e:
            print(f"Error al decodificar el JSON: {e}")
            return

    # Asegurarse de que data es una lista
    if not isinstance(data, list):
        data = [data]

    print(f"Se encontraron {len(data)} conversaciones")

    # Procesar cada conversación
    for i, conversation in enumerate(data):
        # Extraer título y fecha
        title = conversation.get('title', f'Conversación_{i + 1}')
        # Limpiar el título para usarlo como nombre de archivo
        safe_title = "".join([c if c.isalnum() or c in " -_" else "_" for c in title])

        # Obtener fecha de la conversación
        create_time = conversation.get('create_time')
        if create_time:
            # Convertir timestamp a fecha
            date_str = datetime.fromtimestamp(create_time).strftime('%Y-%m-%d')
        else:
            date_str = datetime.now().strftime('%Y-%m-%d')

        # Crear nombre de archivo
        file_name = f"{date_str} {safe_title}"

        # Guardar como JSON
        json_file_path = os.path.join(output_dir, f"{file_name}.json")
        with open(json_file_path, 'w', encoding='utf-8') as f:
            json.dump(conversation, f, ensure_ascii=False, indent=2)

        print(f"Guardado: {json_file_path}")

        # Si se solicita, también exportar como Markdown
        if export_markdown:
            markdown_content = convert_to_markdown(conversation)
            md_file_path = os.path.join(output_dir, f"{file_name}.md")
            with open(md_file_path, 'w', encoding='utf-8') as f:
                f.write(markdown_content)
            print(f"Guardado: {md_file_path}")


def convert_to_markdown(conversation):
    """
    Convierte una conversación a formato Markdown.

    Args:
        conversation (dict): Conversación a convertir

    Returns:
        str: Contenido en formato Markdown
    """
    markdown = f"# {conversation.get('title', 'Conversación')}\n\n"

    # Obtener mensajes ordenados
    messages = get_ordered_messages(conversation)

    # Agregar cada mensaje al Markdown
    for message in messages:
        if not message or not message.get('author'):
            continue

        role = message['author'].get('role')
        if role not in ['user', 'assistant']:
            continue

        role_display = "**Usuario:**" if role == 'user' else "**Asistente:**"
        markdown += f"{role_display}\n\n"

        if message.get('content') and message['content'].get('parts'):
            content = "\n".join(message['content']['parts'])
            markdown += f"{content}\n\n"

    return markdown


def get_ordered_messages(conversation):
    """
    Obtiene los mensajes de una conversación en orden.

    Args:
        conversation (dict): Conversación de la que extraer mensajes

    Returns:
        list: Lista de mensajes ordenados
    """
    ordered_messages = []
    mapping = conversation.get('mapping', {})

    if not mapping:
        return ordered_messages

    # Encontrar el nodo raíz
    root_node_id = None
    for node_id, node in mapping.items():
        if node.get('parent') is None:
            root_node_id = node_id
            break

    if not root_node_id:
        return ordered_messages

    # Función recursiva para recorrer el árbol
    def traverse_tree(node_id):
        node = mapping.get(node_id)
        if not node:
            return

        if node.get('message'):
            ordered_messages.append(node['message'])

        if node.get('children'):
            for child_id in node['children']:
                traverse_tree(child_id)

    # Comenzar recorrido desde el nodo raíz
    traverse_tree(root_node_id)

    return ordered_messages


def main():
    parser = argparse.ArgumentParser(
        description='Separa un archivo JSON de conversaciones de ChatGPT en archivos individuales.')
    parser.add_argument('input_file', help='Archivo JSON de entrada con las conversaciones')
    parser.add_argument('-o', '--output-dir', default='output', help='Directorio de salida para los archivos generados')
    parser.add_argument('-m', '--markdown', action='store_true', help='Exportar también en formato Markdown')

    args = parser.parse_args()

    process_conversations(args.input_file, args.output_dir, args.markdown)
    print(f"Proceso completado. Los archivos se guardaron en: {args.output_dir}")


if __name__ == "__main__":
    main()