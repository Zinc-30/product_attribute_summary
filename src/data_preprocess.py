import gzip
import json
import os
def extract_doc(zipfile_path,basedir):
	"""
		extract text from review dataset
	"""
	zip_file = gzip.open(os.path.join(basedir,zipfile_path), 'r')
	total_fname = os.path.join(basedir,zipfile_path.split('.')[0] + '_total.txt')
	reviews_peritem = {}
	with open(total_fname,"w",encoding='utf-8') as fout:
		for l in zip_file:
			x = json.loads(l)
			rid = x[u'reviewerID']
			pid = x[u'asin']
			rtext = x[u'reviewText']
			if pid not in reviews_peritem:
				reviews_peritem[pid] = []
			reviews_peritem[pid].append(rtext)
			fout.write(rtext+'\n')
	for pid in reviews_peritem:
		item_fname = os.path.join(basedir,zipfile_path.split('.')[0] + '_item_'+pid+'.txt')
		with open(item_fname,"w",encoding='utf-8') as fout:
			for rtext in reviews_peritem[pid]:
				fout.write(rtext+'\n')


if __name__ == '__main__':
	config_file = "../config/default.json"
	with open(config_file) as file:
		config = json.load(file)
	for f in config['zipfiles']:
		extract_doc(f,config['data_dir'])
