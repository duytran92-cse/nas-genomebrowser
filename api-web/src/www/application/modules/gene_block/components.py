
from application.models import *

class GeneBlockHelper(object):
    def load_gene_block(self, id):
        gene_block = GeneBlock.objects.get(pk=id)
        data = {}
        gene = Gene.objects.get(pk=gene_block.gene_id)
        data['gene_title'] = gene.title
        data['id'] = gene_block.id
        data['gene_id'] = gene_block.gene_id
        data['kind'] = gene_block.kind
        data['position'] = gene_block.position
        data['title'] = gene_block.title
        data['sort_order'] = gene_block.sort_order
        if gene_block.kind == 'general_text':
            gene_block_version = GeneBlockVersion.objects.filter(gene_block_id=gene_block.id).filter(version_status='active').order_by('-created_at')
            if gene_block_version:
                data['title'] = gene_block_version[0].title
                data['text'] = gene_block_version[0].text
            else:
                data['title'] = 'No Version avaliable'
                data['text'] = 'No Version avaliable'
        if gene_block.kind == 'general_publications':
            publications = []
            gene_block_version = GeneBlockPublicationVersion.objects.filter(gene_block_id=gene_block.id).filter(version_status='active').order_by('-created_at')
            if gene_block_version:
                rows = GeneBlockPublication.objects.filter(gene_block_id=gene_block.id, gene_block_version_id=gene_block_version[0].id).all()
                for r in rows:
                    publications.append({
                        'id':         r.id,
                        'pmid':       r.pmid,
                        'doi':        r.doi,
                        'pmc':        r.pmc,
                        'title':      r.title,
                        'authors':    r.authors,
                        'journal':    r.journal
                    })
            data['publications'] = publications
        if gene_block.kind == 'gene_effect':
            effects = []
            gene_block_version = GeneBlockEffectVersion.objects.filter(gene_block_id=gene_block.id).filter(version_status='active').order_by('-created_at')
            if gene_block_version:
                rows = GeneBlockEffect.objects.filter(gene_block_id=gene_block.id, gene_block_version_id=gene_block_version[0].id).all()
                for r in rows:
                    effects.append({
                        'id':           r.id,
                        'type':         r.type,
                        'effect':       r.effect,
                        'evidences':    r.evidences,
                        'publication':  r.publication
                    })
            data['effects'] = effects
        if gene_block.kind == 'gene_infobox':
            infobox = []
            gene_block_version = GeneBlockInfoboxVersion.objects.filter(gene_block_id=gene_block.id).filter(version_status='active').order_by('-created_at')
            if gene_block_version:
                rows = GeneBlockInfobox.objects.filter(gene_block_id=gene_block.id, gene_block_version_id=gene_block_version[0].id).all()
                for r in rows:
                    infobox.append({
                        'description':       r.description,
                        'chromosome':        r.chromosome,
                        'start':             r.start,
                        'end':               r.end,
                        'number_of_exons':   r.number_of_exons,
                        'protein_products':  r.protein_products
                    })
            data['infobox'] = infobox
        if gene_block.kind == 'general_alias':
            alias = []
            gene_block_version = GeneBlockAliasVersion.objects.filter(gene_block_id=gene_block.id).filter(version_status='active').order_by('-created_at')
            if gene_block_version:
                rows = GeneBlockAlias.objects.filter(gene_block_id=gene_block.id, gene_block_version_id=gene_block_version[0].id).all()
                for r in rows:
                    alias.append({
                        'alias':           r.alias,
                    })
            data['alias'] = alias
        return data
