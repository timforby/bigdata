import os
import matplotlib.pyplot as plt

def loss_curve(tr, te, OUT_NAME):
	os.makedirs("losses", exist_ok=True)
	plt.figure(figsize=(12, 8))
	plt.plot(tr, label='train')
	plt.plot(te, label='validation')
	plt.legend(prop={'size': 15})
	plt.xlabel('Epoch')
	plt.ylabel('Error')
	d = os.path.join("losses", OUT_NAME)
	plt.savefig(d)
	plt.close('all')
