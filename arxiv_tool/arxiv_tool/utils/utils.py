import os
from pathlib import Path


def construct_md_main_title(arxiv_meta):
    _id = arxiv_meta._id
    title = arxiv_meta.title
    author = arxiv_meta.authors[0]
    return f'{_id}. **{title}**. {author} et al'


def construct_md_link(text, link):
    return f'\[[{text}]({link})\]'


def construct_md_line(arxiv_meta):
    return f'{construct_md_main_title(arxiv_meta)} | {construct_md_link("abs", arxiv_meta.abs_url)}'


def construct_pdf_name(arxiv_meta):
    return get_pdf_name_from_md_main_title(
               construct_md_main_title(arxiv_meta)
           ).replace(':', '#').replace('?', '$').replace(' ', '_')


def get_pdf_name_from_md_main_title(md_main_title):
    return md_main_title.replace('. ', '_').replace('**', '') + '.pdf'


def relpath_from_b_to_a(a_path, b_path):
    common_parent = os.path.commonpath([a_path, b_path])
    a_rel_path = os.path.relpath(a_path, common_parent)
    b_rel_path = os.path.relpath(b_path, common_parent)
    return  '../' * a_rel_path.count('/') + b_rel_path    


def join_relpath(a_path, b_relpath):
    return str(Path(a_path).parents[b_relpath.count('../')] / b_relpath.replace('../', ''))
