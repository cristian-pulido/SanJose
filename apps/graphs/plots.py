from plotly.offline import plot
from plotly.subplots import  make_subplots
import plotly.graph_objs as go 
import pandas as pd 
from datetime import datetime
import requests
from apps.paciente.models import Candidato
import numpy as np
import plotly.express as px
import os



def num_sujetos():
  C=Candidato.objects.all()
  total=len(C)
  inscritos=sum(C.values_list("inscrito",flat=True))
  no_inscritos=total-inscritos
  imagen=(np.array(list(C.values_list('parametrosmotioncorrect',flat=True))) != None).sum()

  fig = make_subplots(rows=1, cols=3, 
					  specs=[[{'type':'domain'}, {'type':'domain'},{'type':'domain'}]],
					  subplot_titles=['Total Candidatos', 'Incluidos','Excluidos']
					 )
  fig.add_trace(go.Pie(labels=["Total Candidatos"], values=[total], text=[total]),  1, 1)
  fig.add_trace(go.Pie(labels=["Incluidos con imagen","Incluidos sin imagen"],
					   values=[imagen,inscritos-imagen], 
					   text=[imagen,inscritos-imagen]),  1, 2)
  fig.add_trace(go.Pie(labels=["Excluidos"], values=[no_inscritos], text=[no_inscritos]),  1, 3)


  fig.update_traces( hoverinfo=["label","label","label"],
					textinfo="text",textfont=dict(size=30)
				   )
  fig['layout'].update(legend=dict(orientation="h"),margin={'t': 20})
		
  plot_div = plot(fig, output_type='div',filename='num_sujetos')

  return plot_div



def time_line_sujetos():
	C=Candidato.objects.all()
  
	data=pd.DataFrame(C.values_list("inscrito",'parametrosmotioncorrect','fecha_de_registro'),columns=['Incluido','Imagen','Fecha'])  
	data['Imagen']=(data.Imagen > 0)
	data['Fecha']=pd.to_datetime(data.Fecha)
	data['Fecha']=data.Fecha.dt.to_period('M')
	g=data.groupby('Fecha')
	data=g.sum()
	data['Candidatos']=g.count()['Incluido']
	t=data.reset_index()


	fig = go.Figure(
		data=[
			go.Scatter(
				name="Incluidos",
				x=t['Fecha'].astype(str),
				y=t['Incluido'],  
				mode="lines+markers",
				text=t['Imagen'],
				hovertemplate="Incluidos: %{y}, Con Imagen: %{text}",
				textposition="top center",
			),
			
			go.Scatter(
				name="Candidatos",
				x=t['Fecha'].astype(str),
				y=t.Candidatos,         
				mode="lines+markers",
						 
			),
			
			
				   
		],
		layout={
			"legend":dict(orientation="h"),
			"xaxis":go.layout.XAxis(
				rangeselector=dict(
					buttons=list([
						dict(count=1,
							label="1 mes",
							step="month",
							stepmode="backward"),
						dict(count=6,
							label="6 meses ",
							step="month",
							stepmode="backward"),

						dict(count=1,
							label="1 año",
							step="year",
							stepmode="backward"),
						dict(step="all")
					])
				),
				rangeslider=dict(
					visible=True
				),
				type="date"
			)
			
		}
	)
	fig['layout'].update(margin={'t': 15})
	plot_div = plot(fig, output_type='div',filename='time_line_sujetos')

	return plot_div

def motivo_exclusion():
	from apps.paciente.templatetags.scripts import mexclusion
	C=Candidato.objects.filter(inscrito=False)
	m_ex=[mexclusion(c) for c in C]
	labels,values=np.unique(m_ex,return_counts=True)

	fig = go.Figure(data=[go.Pie(labels=labels,
                             	 values=values,
                               hole=0.3
                            	)
  											] 
  								)
	fig['layout'].update(legend=dict(orientation="h"),margin={'t': 15})
	plot_div = plot(fig, output_type='div',filename='motivo_exclusion')

	return plot_div

def D_previo_hist():
	C=Candidato.objects.filter(inscrito=False)
	D=[]
	for c in C:
		d_previo=list(c.D_neuro_logico_psiquiatrico_previo.all().values_list('nombre',flat=True))
		if len(d_previo) > 0:
			D+=d_previo
            
	labels,frec=np.unique(D,return_counts=True)
	count_sort_ind = np.argsort(-frec)
	
	labels=labels[count_sort_ind]
	frec=frec[count_sort_ind]
	percent=np.around(frec/frec.sum(),2)
	            
	fig = go.Figure(data=[go.Bar(x=labels, y=frec,
                                 text=frec,
                                 textposition='auto',
                                 hovertext=[str(p*100)+"%" for p in percent])])   
    
	fig['layout'].update(legend=dict(orientation="h"),margin={'t': 15})
	plot_div = plot(fig, output_type='div',filename='D_previo_hist')

	return plot_div

def D_especifico():
	from django.conf import settings
	from wordcloud import WordCloud
	import matplotlib as mpl
	import matplotlib.pyplot as plt
	C=Candidato.objects.filter(inscrito=False)
	media=settings.MEDIA_ROOT    
	folder_words=os.path.join(media,'word_clouds')
    
	if not os.path.exists(os.path.join(folder_words,'wordcloud_D_Especifico'+str(len(C))+'.svg')):
		for i in os.listdir(folder_words):
			if i.startswith("wordcloud_D_Especifico"):
				os.remove(os.path.join(folder_words,i))
		especificos=list(C.values_list('D_especificos',flat=True))
		especificos=[i for i in especificos if i !='']
		W=' '.join(especificos)
		W=W.replace('de', '').replace('Antecedente', '').replace('en', '')
		wordcloud = WordCloud(
		                      background_color='white',
		                      max_words=200,
		                      max_font_size=40, 
		                      width=400, height=300,
		                      random_state=42
		                     ).generate(W)  
		plt.imshow(wordcloud)
		plt.axis('off')

		plt.savefig(os.path.join(folder_words,'wordcloud_D_Especifico'+str(len(C))+'.svg'),dpi=400)
    

	return os.path.join("/media/word_clouds",'wordcloud_D_Especifico'+str(len(C))+'.svg')

def demografico_continuo():
	from apps.paciente.models import Ingreso
	I=Ingreso.objects.filter(candidato__inscrito = True)
	T=pd.DataFrame(I.values_list("candidato__edad","peso",'estatura'),columns=['Edad','Peso (Kgs)','Estatura (cms)'])
	data=pd.DataFrame()
	data['valor']=T.values.flatten()
	data['Variable']=list(T.columns.values)*len(T)
    
	fig = px.violin(data,y='valor',color='Variable',box=True,points='all')
	fig['layout'].update(margin={'t': 15})
	plot_div = plot(fig, output_type='div',filename='demografico_continuo')

	return plot_div

def demografico_categorical():
	from apps.paciente.models import Ingreso
	I=Ingreso.objects.filter(candidato__inscrito = True)
	T=pd.DataFrame(I.values_list("candidato__sexo","lateralidad",'n_educativo'),columns=['Sexo','Lateralidad','Nivel Educativo'])
	data=pd.DataFrame()
	data['valor']=T.values.flatten()
	data['Variable']=list(T.columns.values)*len(T)
	fig = px.histogram(data,x='valor',color='Variable')
	fig['layout'].update(margin={'t': 15})
	plot_div = plot(fig, output_type='div',filename='demografico_categorical')

	return plot_div

def demografico_map():
	from apps.paciente.models import Ingreso    
	municipio=pd.read_csv("/home/colciencias/SanJose/apps/graphs/municipioscolombia.csv",index_col='ciudad')
	inscrito=Ingreso.objects.filter(candidato__inscrito = True)
	lugar=pd.DataFrame(inscrito.values_list("lugar_nacimiento","lugar_residencia"),columns=['nacimiento','residencia'])
	lugar['nacimiento']=[i.split(', ')[-1] for i in lugar.nacimiento]
	lugar['residencia']=[i.split(', ')[-1] for i in lugar.residencia]
    
	lugares=pd.DataFrame()
	lugares['Ciudad']=np.concatenate((lugar.nacimiento,lugar.residencia))
	lugares['Lugar']=['nacimiento']*len(lugar)+['residencia']*len(lugar)
	filter_c=municipio.loc[lugares.Ciudad].reset_index()
	filter_c['Lugar']=lugares.Lugar
	X=filter_c.groupby(filter_c.columns.tolist(),as_index=False).size().reset_index().rename(columns={0:'Frecuencia'})
                                     

	px.set_mapbox_access_token("pk.eyJ1IjoiY3B1bGlkbzk0IiwiYSI6ImNqejNxMXFoaTA0MzgzY3MxOHVnZTkwcGMifQ.-dGFAmjoYPK9kXWSrAbBqg")
	fig = px.scatter_mapbox(X, lat="latitude", lon="longitude",hover_data=['ciudad','departamento'],zoom=4,color='Lugar',size='Frecuencia')
	fig['layout'].update(margin={'t': 15})
	plot_div = plot(fig, output_type='div',filename='demografico_map')

	return plot_div


def demografico_multi_scatter():
	from apps.paciente.models import Ingreso
	I=Ingreso.objects.filter(candidato__inscrito = True)  
	T=pd.DataFrame(I.values_list("candidato__edad","peso",'estatura','candidato__sexo','lateralidad','n_educativo'),columns=['Edad','Peso (Kgs)','Estatura (cms)','Sexo','Lateralidad','Nivel Educativo'])
	fig = px.scatter(T,x='Estatura (cms)',y='Peso (Kgs)',color='Sexo',
                     size='Edad',facet_col='Nivel Educativo',
                     marginal_x='box',marginal_y='box')
	fig['layout'].update(margin={'t': 15})
	plot_div = plot(fig, output_type='div',filename='demografico_multi_scatter')
	return plot_div


def demografico_multi_categorical():
	from apps.paciente.models import Ingreso
	I=Ingreso.objects.filter(candidato__inscrito = True)  
	T=pd.DataFrame(I.values_list("candidato__edad","peso",'estatura','candidato__sexo','lateralidad','n_educativo'),columns=['Edad','Peso (Kgs)','Estatura (cms)','Sexo','Lateralidad','Nivel Educativo'])


	fig = px.parallel_categories(T,color='Edad')
	fig['layout'].update(margin={'t': 15})

	plot_div = plot(fig, output_type='div',filename='demografico_multi_categorical')

	return plot_div


def clinica_grupod():
  C=Candidato.objects.filter(inscrito=True)
  G=C.values_list('G_diagnostico',flat=True)
  labels,values=np.unique(G,return_counts=True)

  fig = go.Figure(data=[go.Pie(labels=labels,
                             	 values=values,
                               hole=0.3,
                               text=labels,
                               hoverinfo='text+value'
                            	)
  											] 
  								)
  fig['layout'].update(legend=dict(orientation="h"),margin={'t': 15})

  plot_div = plot(fig, output_type='div',filename='clinica_grupod')
  return plot_div

def clinica_conciencia():
	from apps.paciente.models import Ingreso
	I=Ingreso.objects.filter(candidato__inscrito = True)  
	conciencia=I.values_list("conciencia",flat=True)

	labels,values=np.unique(conciencia,return_counts=True)

	fig = go.Figure(data=[go.Pie(labels=labels,
                                 values=values,
                                 hole=0.3,
                                 text=labels,
                                 hoverinfo='text+value'
                                 )
                          ] 
                    )
	fig['layout'].update(legend=dict(orientation="h"),margin={'t': 15})

	plot_div = plot(fig, output_type='div',filename='clinica_conciencia')
	return plot_div

def clinica_a_patologicos():
	from apps.paciente.models import Ingreso    
	C=Ingreso.objects.all()
	P=[]
	for c in C:
		patologico=list(c.a_patologicos.all().values_list('nombre',flat=True))
		if len(patologico) > 0:
			P+=patologico
            
	labels,frec=np.unique(P,return_counts=True)
	count_sort_ind = np.argsort(-frec)
	
	labels=labels[count_sort_ind]
	frec=frec[count_sort_ind]
	percent=np.around(frec/frec.sum(),2)
	            
	fig = go.Figure(data=[go.Bar(x=labels, y=frec,
                                 text=frec,
                                 textposition='auto',
                                 hovertext=[str(p*100)+"%" for p in percent])])   
    
	fig['layout'].update(legend=dict(orientation="h"),margin={'t': 15})
	plot_div = plot(fig, output_type='div',filename='clinica_a_patologicos')

	return plot_div

def clinica_antecedentes():
    
	from django.conf import settings
	from wordcloud import WordCloud
	import matplotlib as mpl
	import matplotlib.pyplot as plt
	from apps.paciente.models import Ingreso    
	I=Ingreso.objects.all()
	media=settings.MEDIA_ROOT    
	folder_words=os.path.join(media,'word_clouds')
    
	antecedentes = ['a_patologicos_cual','a_toxico_alergenicos','a_familiares']
	files=[os.path.join(folder_words,'wordcloud_'+i+str(len(I))+'.svg') for i in antecedentes]    
	existencia=[os.path.exists(i) for i in files]
    
	if np.sum(existencia) != 3:
		for i in os.listdir(folder_words):
			if i.startswith("wordcloud_a_patologicos_cual") or i.startswith("wordcloud_a_toxico_alergenicos") or i.startswith("wordcloud_a_familiares"):
				os.remove(os.path.join(folder_words,i))


			for i in antecedentes:
				W=" ".join([k for k in list(I.values_list(i,flat=True)) if k])
				wordcloud = WordCloud(
				                      background_color='white',
				                      max_words=200,
				                      max_font_size=40, 
				                      width=400, height=300,
				                      random_state=42
				                     ).generate(W)  
				plt.imshow(wordcloud)
				plt.axis('off')

				plt.savefig(os.path.join(folder_words,'wordcloud_'+i+str(len(I))+'.svg'),dpi=400)        

	return [os.path.join("/media/",'word_clouds/wordcloud_'+i+str(len(I))+'.svg') for i in antecedentes]





def clinica_uci_g():
	from apps.paciente.models import Uci  
	U=Uci.objects.filter(candidato__inscrito = True)
	glasgow=pd.DataFrame(U.values_list("glasgowtotal",flat=True),columns=['Glasgow Total Ingreso'])
	fig = px.box(glasgow,y='Glasgow Total Ingreso')
	fig['layout'].update(margin={'t': 15})  


	plot_div = plot(fig, output_type='div',filename='clinica_uci_g')
	return plot_div

def clinica_uci_egreso():
	from apps.paciente.models import Uci  
	U=Uci.objects.filter(candidato__inscrito = True)
	egreso=pd.DataFrame(U.values_list('condicion_egreso'),columns=['Condición de Egreso']).dropna()
	fig = px.histogram(egreso,x='Condición de Egreso')
	fig['layout'].update(margin={'t': 15})  


	plot_div = plot(fig, output_type='div',filename='clinica_uci_egreso')
	return plot_div

def clinica_formularios():
	C=Candidato.objects.filter(inscrito=True)
	D=pd.DataFrame(C.values_list('neurologia','informante','moca','neuropsi','lectura_resonancia'))
	x=(D[~(D[4].duplicated() & ~D[4].isna())]>0).sum().values
	y=['Neurología','Neuropsicología Informante','Moca','Neuropsi','Lectura Estructural']
	lista=[]
	for i in range(len(x)):
		lista+=[y[i]]*x[i]
  
	fig = go.Figure(data=[go.Histogram(x=lista)])
	fig['layout'].update(legend=dict(orientation="h"),margin={'t': 15})

	plot_div = plot(fig, output_type='div',filename='clinica_formularios')
	return plot_div

def uci_glasgow_ingreso():
    from apps.paciente.models import Uci
    U=Uci.objects.filter(candidato__inscrito=True)
    
    A=pd.DataFrame(U.values_list('apertura_ocular','respuesta_motora','respuesta_verbal','glasgowtotal'),columns=['Apertura ocular','Respuesta motora','Respuesta Verbal','Glasgow Total ingreso'])
    A=A.astype(int)
    
    fig=px.parallel_categories(A,color='Glasgow Total ingreso')
    fig['layout'].update(margin={'t': 15})
    
    plot_div = plot(fig, output_type='div',filename='uci_glasgow_ingreso')
    return plot_div

def uci_variables_vs_egreso():
    from apps.paciente.models import Uci
    U=Uci.objects.filter(candidato__inscrito=True)
    A=pd.DataFrame(U.values_list('fallaorganica','sepsis',
                                'presion_intracraneana','monitoria_pic',
                                'ventilacionmecanica','soportevasopresor',
                                'condicion_egreso'),
                   columns=['Falla Organica','Sepsis','Presión Intracraneana',
                            'Monitoria Pic','Ventilación Mecanica',
                            'Soporte Vasopresor','Condición Egreso'])
        
    fig=px.parallel_categories(A)
    fig['layout'].update(margin={'t': 15})
    
    plot_div = plot(fig, output_type='div',filename='uci_variables_vs_egreso')
    return plot_div

def uci_falla_organica():
	from apps.paciente.models import Uci   
	U=Uci.objects.filter(candidato__inscrito=True)
	F=[i for i in list(U.values_list('fallaorganica_cual',flat=True)) if i]

            
	labels,frec=np.unique(F,return_counts=True)
	count_sort_ind = np.argsort(-frec)
	
	labels=labels[count_sort_ind]
	frec=frec[count_sort_ind]
	percent=np.around(frec/frec.sum(),2)
	            
	fig = go.Figure(data=[go.Bar(x=labels, y=frec,
                                 text=frec,
                                 textposition='auto',
                                 hovertext=[str(p*100)+"%" for p in percent])])   
    
	fig['layout'].update(legend=dict(orientation="h"),margin={'t': 15})
	plot_div = plot(fig, output_type='div',filename='uci_falla_organica')

	return plot_div

def uci_glasgow_egreso():
    from apps.paciente.models import Uci
    U=Uci.objects.filter(candidato__inscrito=True).exclude(condicion_egreso = 'Fallecido')    
    A=pd.DataFrame(U.values_list('apertura_ocular_e','respuesta_motora_e',
                                 'respuesta_verbal_e','glasgowtotal_e'),
                   columns=['Apertura ocular','Respuesta motora',
                            'Respuesta Verbal','Glasgow Total Egreso'])
    A=A[A['Glasgow Total Egreso']!='0'].astype(int)
     
    fig=px.parallel_categories(A,color='Glasgow Total Egreso')
    fig['layout'].update(margin={'t': 15})
    
    plot_div = plot(fig, output_type='div',filename='uci_glasgow_egreso')
    return plot_div

def uci_causa_mortalidad():
	from apps.paciente.models import Uci   
	U=Uci.objects.filter(candidato__inscrito=True)
	F=[i for i in list(U.values_list('causa_mortalidad',flat=True)) if i]
    
	for i in range(len(F)):
		F[i]=F[i].lower()

            
	labels,frec=np.unique(F,return_counts=True)
	count_sort_ind = np.argsort(-frec)
	
	labels=labels[count_sort_ind]
	frec=frec[count_sort_ind]
	percent=np.around(frec/frec.sum(),2)
	            
	fig = go.Figure(data=[go.Bar(x=labels, y=frec,
                                 text=frec,
                                 textposition='auto',
                                 hovertext=[str(p*100)+"%" for p in percent])])   
    
	fig['layout'].update(legend=dict(orientation="h"),margin={'t': 15})
	plot_div = plot(fig, output_type='div',filename='uci_causa_mortalidad')

	return plot_div

def uci_dx_egreso():
    
	from django.conf import settings
	from wordcloud import WordCloud
	import matplotlib as mpl
	import matplotlib.pyplot as plt
	from apps.paciente.models import Uci   
	U=Uci.objects.filter(candidato__inscrito=True)
	E=len(U.filter(glasgowtotal_e = 0))
	media=settings.MEDIA_ROOT    
	folder_words=os.path.join(media,'word_clouds')
    
	file=os.path.join(folder_words,'wordcloud_uci_dx_egreso'+str(len(U))+str(E)+'.svg')

    
	if not os.path.exists(file):
		for i in os.listdir(folder_words):
			if i.startswith("wordcloud_uci_dx_egreso"):
				os.remove(os.path.join(folder_words,i))
		W=" ".join([i for i in list(U.values_list('dx_egreso',flat=True)) if i])
		wordcloud = WordCloud(
		                      background_color='white',
		                      max_words=200,
		                      max_font_size=40, 
		                      width=400, height=300,
		                      random_state=42
		                     ).generate(W)  
		plt.imshow(wordcloud)
		plt.axis('off')

		plt.savefig(os.path.join(folder_words,'wordcloud_uci_dx_egreso'+str(len(U))+str(E)+'.svg'),dpi=400)        

	return os.path.join("/media/",'word_clouds/wordcloud_uci_dx_egreso'+str(len(U))+str(E)+'.svg')
    


def neurologia_crsr():
    C=Candidato.objects.filter(inscrito = True)
    N=[c.neurologia_set.last() for c in C]
    
    auditiva_values=['No hay respuesta','Percibe pero no localiza (Sobresalto auditivo)','Localiza el sonido','Reproduce movimiento a la orden','Movimiento consistente a la orden']
    
    motora_values=['No hay respuesta/flacidez','Postura anormal','Retirada flexora','Localización de estímulos dolorosos','Manipulación de objetos','Respuesta motora automática','Uso funcional del objeto']
    
    comunicacion_values=['No hay respuesta','No funcional: Intencional','Funcional: Adecuada']
    
    visual_values=['No hay respuesta','Sobresalto visual','Fijación visual','Seguimiento visual','Localiza el objeto: alcanza','Reconoce el objeto']
    
    verbal_values=['No hay respuesta','Movimientos orales reflejos','Movimientos orales/vocalizaciones','Verbalización entendible']
    
    alerta_values=['No hay respuesta','Apertura ocular con estimulación','Apertura ocular espontánea','Alerta y atento']   
        
    cols=[['AUDITIVA','auditiva',auditiva_values],['MOTORA','motora',motora_values],['COMUNICACIÓN','comunicacion',comunicacion_values],['VISUAL','visual',visual_values],['OROMOTORA/VERBAL','verbal',verbal_values],['NIVEL DE ALERTA','alerta',alerta_values]]
    
    A=pd.DataFrame()
    
    for i in cols:
        A[i[0]]=["("+str(int(getattr(j,i[1])))+")" for j in N if j] #+" "+i[2][int(getattr(j,i[1]))]
        
    A['Total']=[int(i.total1) for i in N if i ]
    
    A=A.dropna()    
    fig=px.parallel_categories(A,color='Total')
    fig['layout'].update(margin={'t': 15})
    
    plot_div = plot(fig, output_type='div',filename='neurologia_crsr')
    return plot_div



def neurologia_four():
    C=Candidato.objects.filter(inscrito = True)
    N=[c.neurologia_set.last() for c in C]
    
    ocular_values=['Ojos cerrados al dolor','Apertura a estímulos nociceptivos','Apertura a estímulos sonoros intensos','Espontánea pero no dirige la mirada','Dirige la mirada en respuesta a órdenes']
    
    motora_values=['Ninguna o Estado mioclónico generalizado','Respuesta extensora al dolor (Descerebración)','Respuesta flexora al dolor en MMSS (Decorticación y retirada)','Localiza estímulos dolorosos','Obedece órdenes']
    
    tronco_values=['Reflejos corneales, fotomotores y tusígeno ausentes','Reflejos corneales y fotomotores ausentes','Reflejos corneales o fotomotores ausentes','Reflejo motor ausente unilateral','Ambos reflejos corneales y fotomotores presentes']  
    
    respiracion_values=['Intubado, respira a la frecuencia del respirador o apnea','Intubado, respira por encima de la frecuencia del respirador','No intubado, respiración irregular','No intubado, respiración de Cheyene- Stokes','No intubado, respiración rítmica']
        
    cols=[['Apertura ocular','aperturaocular',ocular_values],['Respuesta Motora','respuestamotora',motora_values],['Reflejos del Tronco','reflejos',tronco_values],['Respiración','respiracion',respiracion_values]]
    
    A=pd.DataFrame()
    
    for i in cols:
        A[i[0]]=["("+str(int(getattr(j,i[1])))+")" for j in N if j] #+" "+i[2][int(getattr(j,i[1]))]
        
    A['Total']=[int(i.total2) for i in N if i ]
    
    Resultado=['Severa injuria cerebral']*8+['Moderada injuria cerebral']*5+['Leve injuria cerebral']*4
    A['Resultado']=np.array(Resultado)[A.Total]
    
    A=A.dropna()    
    fig=px.parallel_categories(A,dimensions=[i[0] for i in cols]+['Resultado'],color='Total')
    fig['layout'].update(margin={'t': 15})
    plot_div = plot(fig, output_type='div',filename='neurologia_four')
    return plot_div

def neurologia_conciencia():
	C=Candidato.objects.filter(inscrito = True)
	N=[c.neurologia_set.last() for c in C]  
	F=[i.estadoconciencia for i in N if i]
               
	labels,frec=np.unique(F,return_counts=True)
	count_sort_ind = np.argsort(-frec)
	
	labels=labels[count_sort_ind]
	frec=frec[count_sort_ind]
	percent=np.around(frec/frec.sum(),2)
	            
	fig = go.Figure(data=[go.Bar(x=labels, y=frec,
                                 text=frec,
                                 textposition='auto',
                                 hovertext=[str(p*100)+"%" for p in percent])])   
    
	fig['layout'].update(legend=dict(orientation="h"),margin={'t': 15})
	plot_div = plot(fig, output_type='div',filename='neurologia_conciencia')

	return plot_div

def neurologia_vs():
    
    C=Candidato.objects.filter(inscrito = True)
    N=[c.neurologia_set.last() for c in C]    
    scale=[int(i.total1) for i in N if i ]
    four=[int(i.total2) for i in N if i ]
    Resultado=['Severa injuria cerebral']*8+['Moderada injuria cerebral']*5+['Leve injuria cerebral']*4
    four_=np.array(Resultado)[four]
    F=[i.estadoconciencia for i in N if i]    
    A=pd.DataFrame()
    A['CRSR']=scale
    A['FOUR']=four_
    A['Estado de Conciencia']=F
    fig=px.strip(data_frame=A,x='FOUR',y='CRSR',
                 color='Estado de Conciencia',
                 category_orders={'FOUR':['Leve injuria cerebral',
                                          'Moderada injuria cerebral',
                                          'Severa injuria cerebral']})
    fig['layout'].update(legend=dict(orientation="v"),margin={'t': 15})
    plot_div = plot(fig, output_type='div',filename='neurologia_vs')
  
    return plot_div



def neuropsi_vs_G_diagnostico():
  from apps.paciente.models import Neuropsi
  N=Neuropsi.objects.all()

  A=pd.DataFrame([[n.candidato.G_diagnostico,n.orientacion,n.atencion,n.codificacion,n.evocacion] for n in N], 
  	columns=['Grupo Diagnóstico','Orientación','Atención','Codificación','Evocación']).dropna()
  fig=px.parallel_categories(A)

  fig['layout'].update(margin={'t': 15})
  plot_div = plot(fig, output_type='div',filename='neuropsi_vs_G_diagnostico_2')
  
  return plot_div


def informante_all():
    from apps.paciente.models import Informante
    I=Informante.objects.filter(candidato__inscrito = True)
    A=I.values_list("candidato__sexo",'totalindependencia','totalmemoria','totalapatia','totaldes','totalfunciones')
    A=pd.DataFrame(A,columns=['Sexo','Lawton-Brody','Memoria','Apatía','Desinhibición','Funciones Ejecutivas'])
    A['Funciones Ejecutivas']=pd.to_numeric(A['Funciones Ejecutivas'])
    A.to_csv("/home/colciencias/media/n.csv",index=False)
    fig=px.parallel_categories(A,color='Funciones Ejecutivas')
    
    fig['layout'].update(margin={'t': 15})
    plot_div = plot(fig, output_type='div',filename='informante_all')
      
    return plot_div

def moca():
    from apps.paciente.models import Moca
    M=Moca.objects.all()
    A=M.values_list("funcion_visoespacial","identificacion","atencion_numero",
                  "atencion_letras","atencion_resta","lenguaje_repite","lenguaje_fluidez",
                  "abstraccion","recuerdo","orientacion","total")
    A=pd.DataFrame(A,columns=['Funcion Visoespacial','Identificación',
                              'Atención Número','Atención Letras','Atención Resta','Lenguaje Repite',
                              'Lenguaje Fluidez','Abstracción','Recuerdo Diferido','Orientación','Total'])
    A['Total']=pd.to_numeric(A['Total'])
    fig=px.parallel_categories(A,color='Total')
    fig['layout'].update(margin={'t': 15})
    plot_div = plot(fig, output_type='div',filename='moca')

    return plot_div

def results_neuropsicologia():
    from apps.paciente.models import Moca
    M=Moca.objects.all()
    A=M.values_list('total','candidato__neuropsi__resultado',
                  #'candidato__informante__totalindependencia',
                  'candidato__informante__totalmemoria',
                  #'candidato__informante__totalapatia',
                  #'candidato__informante__totaldes',
                  'candidato__informante__totalfunciones'
                   )
    data=pd.DataFrame(A,columns=['Total Moca','Resultado Neuropsi',
                              #'Lawton-Brody',
                              'Memoria (Informante)',
                              #'Apatía',
                              #'Desinhibición',
                              'Funciones Ejecutivas (Informante)'
                             ])
    data['Funciones Ejecutivas (Informante)']=pd.to_numeric(data['Funciones Ejecutivas (Informante)'])
    fig=px.scatter(data,x='Memoria (Informante)',y='Total Moca',color='Resultado Neuropsi',size='Funciones Ejecutivas (Informante)')
    fig['layout'].update(margin={'t': 15})
    plot_div = plot(fig, output_type='div',filename='results_neuropsicologia')

    return plot_div