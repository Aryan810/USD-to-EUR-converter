import tkinter as tk
from urllib.request import Request, urlopen




class MainProgram:
	def __init__ (self, master):
		self.master = master
		self.master.title('USDtoEUR')
		self.master.columnconfigure(0, weight=1)
		
		#fenetre comprenant les éléments de la première ligne de programme
		self.mainframe = tk.Frame(self.master)
		self.mainframe.grid(sticky=tk.N+tk.S+tk.W+tk.E)
		
		self.mainframe.columnconfigure(1, weight=2)	
		self.mainframe.columnconfigure(2, weight=1)
		self.mainframe.columnconfigure(4, weight=2)
		
		#label "source"
		self.sourcelabel = tk.Label(self.mainframe, text='Prix en USD')
		self.sourcelabel.grid(column=0, row=0, padx=3)
		
		#Spinbox d'input utilisateur
		self.input = tk.Spinbox(self.mainframe, width=10, from_=0, to=5000000000, increment=1)
		self.input.delete('0', tk.END)
		self.input.grid(column=1, row=0, sticky=tk.N+tk.S+tk.E+tk.W, padx=5)
		self.input.focus_set()

		#bouton de conversion. Fait appel à la fonction getrate
		self.button = tk.Button(self.mainframe, text="Convertir en EUR", command=self.getrate, width=15)
		self.button.grid(column=2, row=0, padx=5, sticky=tk.N+tk.S+tk.E+tk.W)
		
		#label "résultat"
		self.resultlabel = tk.Label(self.mainframe, text='Résultat en EUR', width=13, anchor=tk.E,)
		self.resultlabel.grid(column=3, row=0)
	
		#box d'affichage de la conversion
		self.resultbox = tk.Text(self.mainframe, height=1, width=10, state='disabled')
		self.resultbox.grid(column=4, row=0, sticky=tk.N+tk.S+tk.E+tk.W, padx=5)
		
		#Fenetre comprenant les éléments de la 2e ligne de programme
		self.bottomframe = tk.Frame(self.master)
		self.bottomframe.grid(row=1, sticky=tk.N+tk.S+tk.W+tk.E)
		
		#Bouton invert
		self.invertbutton = tk.Button(self.bottomframe, text="Inverser sens de conversion", command=self.invert, width=30)
		self.invertbutton.pack(side=tk.LEFT, padx=3, pady=3)

		#Bout quit
		self.quitbutton = tk.Button(self.bottomframe, text='Quitter', command=lambda: self.master.destroy(), width=15)
		self.quitbutton.pack(side=tk.LEFT)

		
	def getrate(self):
		try :
			self.rate
		except AttributeError:
			#self.source = urlopen('http://api.fixer.io/latest').read()
			self.source = str(urlopen('http://devel.farebookings.com/api/curconversor/USD/EUR/1/').read())
			self.source = self.source.replace("'", '').split(' ')
			self.rate = self.source[-1]
		
		self.convert()


	def invert(self):
		#inversion du nom des bouttons
		self.sourcelabel['text'] = 'Prix en EUR' if self.sourcelabel['text'] == 'Prix en USD' else 'Prix en USD'
		self.button['text'] = 'Convertir en USD' if self.button['text'] == 'Convertir en EUR' else 'Convertir en EUR'
		self.resultlabel['text'] = 'Résulat en USD' if self.resultlabel['text'] == 'Résultat en EUR' else 'Résultat en EUR'
		
		#inversion du contenu des box
		self.resultbox['state'] = 'normal'
		self.input.delete('0', tk.END)
		self.input.insert('0', self.resultbox.get('1.0', tk.END).strip())
		self.resultbox.delete('1.0', tk.END)
		self.convert()
		self.resultbox['state'] = 'disabled'
		
		#selection de l'input
		self.input.selection('from', '0')
		self.input.selection('to', tk.END)

	def convert(self):
		try:
			float(self.input.get().replace(',', '.'))
		except ValueError:
			self.input.focus_set()
			self.input.selection('from', '0')
			self.input.selection('to', tk.END)
			self.resultbox['state'] = 'normal'
			self.resultbox.delete('1.0', tk.END)
			self.resultbox['state'] = 'disabled'		
			return
	
		self.inputvalue = float(self.input.get().replace(',', '.'))
		self.result = float(self.rate) * self.inputvalue if self.button['text'] == 'Convertir en EUR' else self.inputvalue / float(self.rate)
		
		self.resultbox['state'] = 'normal'
		self.resultbox.delete('1.0', tk.END)
		self.resultbox.insert('1.0', '{0:.2f}'.format(self.result))
		self.resultbox['state'] = 'disabled'
		
		#selection de l'input
		self.input.focus_set()
		self.input.selection('from', '0')
		self.input.selection('to', tk.END)
		
		
root = tk.Tk()
main = MainProgram(root)
root.tk.mainloop()
