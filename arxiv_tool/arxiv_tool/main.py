import sys
import fire

from pathlib import Path
from loguru import logger

from .utils import (
    arxiv_api, 
    MdFile, 
    PatternRecognizer, 
    PdfDownloader, 
    construct_pdf_name, 
    construct_md_line, 
    construct_md_link, 
    get_pdf_name_from_md_main_title,
    relpath_from_b_to_a,
)


def _download_arxiv_pdf(arxiv_meta, pdf_download_dir='.'):
    pdf_url = arxiv_meta.pdf_url
    pdf_path = Path(pdf_download_dir) / construct_pdf_name(arxiv_meta)
    pdf_path.parent.mkdir(parents=True, exist_ok=True)
    if not pdf_path.exists():
        PdfDownloader().download(pdf_url, pdf_path)
    return pdf_path


def fetch(arxiv_url, pdf_download_dir='./pdfs'):
    arxiv_meta = arxiv_api.fetch(arxiv_url)
    logger.info(f'get paper: {arxiv_meta}')
    _download_arxiv_pdf(arxiv_meta, pdf_download_dir)


def search(key_words, summary_md_file='summary.md', download_pdf=False, pdf_download_dir='./pdfs'):
    arxiv_meta_list = arxiv_api.search(key_words)
    logger.info(f'collect {len(arxiv_meta_list)} papers:')
    for arxiv_meta in arxiv_meta_list:
        logger.info(f'    {arxiv_meta}')

    summary_md_path = Path(pdf_download_dir) / summary_md_file
    with open(summary_md_path, 'w') as f:
        f.write('# Collected Papers\n\n')
        f.write(f'> Key Words: {key_words}\n\n')
        for arxiv_meta in arxiv_meta_list:
            md_line = construct_md_line(arxiv_meta)
            f.write(f'- {md_line}\n')
    logger.info(f'summary file saved to {summary_md_path} ')

    if download_pdf:
        logger.info(f'download pdf files to {pdf_download_dir} ...')
        for arxiv_meta in arxiv_meta_list:
            _download_arxiv_pdf(arxiv_meta, pdf_download_dir)


def _markdown(md_path, download_pdf=False, pdf_download_dir='./pdfs'):
    logger.info(f'Process {md_path} ...')
    increased_item_recognizer = PatternRecognizer('Increased Item Recognizer', r'{{https?://arxiv.org/abs/\d{4}.\d{5}}}')
    existed_item_recognizer = PatternRecognizer('Existed Item Recognizer', r'\d{4}.\d{5}.*et al \| .*')

    main_title_recognizer = PatternRecognizer('main title recognizer', r'\d{4}.\d{5}.*et al')
    abs_url_recognizer = PatternRecognizer('abs url recognizer', r'https?://arxiv.org/abs/\d{4}.\d{5}')
    pdf_path_recognizer = PatternRecognizer('pdf path recognizer', r'\\\[\[pdf\]\((.*)\)\\\]')

    def increased_item_handler(item):
        try:
            arxiv_url = abs_url_recognizer.findall(item)[0]
            arxiv_meta = arxiv_api.fetch(arxiv_url)
            return construct_md_line(arxiv_meta)
        except Exception as e:
            logger.warning(f'{item} failed: {e}')
            return item

    def existed_item_handler(item):
        try:
            main_title = main_title_recognizer.findall(item)[0]
            arxiv_url = abs_url_recognizer.findall(item)[0]
            pdf_relpath_to_md = (pdf_path_recognizer.findall(item) + [None])[0]

            if pdf_relpath_to_md is None:
                pdf_name = get_pdf_name_from_md_main_title(main_title)
                pdf_path = Path(pdf_download_dir) / pdf_name

                if pdf_path.exists():
                    logger.info(f'{item} => no pdf link, but pdf file exists => add pdf link')
                else:
                    logger.info(f'{item} => no pdf link, and pdf file not exists => download and add pdf link')
                    arxiv_meta = arxiv_api.fetch(arxiv_url)
                    _download_arxiv_pdf(arxiv_meta, pdf_download_dir)
                
                pdf_relpath_to_md = relpath_from_b_to_a(md_path.absolute().as_posix(), pdf_path.absolute().as_posix())
                return f"{item} {construct_md_link('pdf', pdf_relpath_to_md)}"
            else:
                pdf_path = md_path.joinpath(pdf_relpath_to_md)
                if Path(pdf_path).exists():
                    logger.info(f'{item} => has pdf link, and pdf file exists => do nothing')
                    return item
                else:
                    logger.info(f'{item} => has pdf link, but pdf file not exists => download and modify pdf link')
                    arxiv_meta = arxiv_api.fetch(arxiv_url)
                    new_pdf_path = _download_arxiv_pdf(arxiv_meta, pdf_download_dir)
                    new_pdf_relpath_to_md = relpath_from_b_to_a(md_path.absolute().as_posix(), new_pdf_path.absolute().as_posix())
                    return item.replace(pdf_relpath_to_md, str(new_pdf_relpath_to_md))

        except Exception as e:
            logger.warning(f'{item} failed: {e}')
            return item

    md_file = MdFile(md_path)

    # 1. 替换为 markdown 格式
    md_file.replace(increased_item_recognizer, increased_item_handler)
    
    # 2. 检查 pdf, 根据情况下载
    if download_pdf:
        md_file.replace(existed_item_recognizer, existed_item_handler)

    md_file.save()


def markdown(md_path_or_dir, download_pdf=False, pdf_download_dir='./pdfs'):
    if Path(md_path_or_dir).is_dir():
        md_paths = list(Path(md_path_or_dir).rglob('*.md'))
    elif Path(md_path_or_dir).is_file() and Path(md_path_or_dir).suffix == '.md':
        md_paths = [Path(md_path_or_dir)]
    else:
        md_paths = []
    
    logger.info(f'Detect {len(md_paths)} markdown files:')
    for md_path in md_paths:
        logger.info(f'    {md_path}')
        _markdown(md_path, download_pdf, pdf_download_dir)


def main():
    logger.remove()
    logger.add(
        sys.stdout,
        level='INFO',
    )
    fire.Fire({
        'fetch': fetch,
        'search': search,
        'markdown': markdown
    })
