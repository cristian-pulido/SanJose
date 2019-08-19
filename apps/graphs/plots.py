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
  fig['layout'].update(legend=dict(orientation="h"))
		
  plot_div = plot(fig, output_type='div',filename='num_sujetos')

  return plot_div



def time_line_sujetos():
  C=Candidato.objects.all()
  inscrito=C.values_list('inscrito',flat=True)
  imagen=np.array(list(C.values_list('parametrosmotioncorrect',flat=True))) != None
  fecha=C.values_list('fecha_de_registro',flat=True)
  data=pd.DataFrame(list(zip(inscrito,fecha,imagen)),columns=['inscrito','fecha_de_registro','imagen'])
  data['fecha_de_registro']=pd.to_datetime(data['fecha_de_registro'])
  tiempo=data[['inscrito','imagen']]
  tiempo['year-mes']=data['fecha_de_registro'].dt.to_period('M')
  t=tiempo.groupby(['year-mes']).sum().reset_index()
  t['candidatos']=tiempo.groupby(['year-mes']).count()['inscrito'].values

  fig = go.Figure(
		data=[
			go.Scatter(
				name="Incluidos",
				x=t['year-mes'].astype(str),
				y=t['inscrito'],  
				mode="lines+markers",
				text=t['imagen'],
				hovertemplate="Incluidos: %{y}, Con Imagen: %{text}",
				textposition="top center",
			),
			
			go.Scatter(
				name="Candidatos",
				x=t['year-mes'].astype(str),
				y=t.candidatos,         
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
	fig['layout'].update(legend=dict(orientation="h"))
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
    
	fig['layout'].update(legend=dict(orientation="h"))
	plot_div = plot(fig, output_type='div',filename='D_previo_hist')

	return plot_div

def D_especifico():
	from django.conf import settings
	from wordcloud import WordCloud
	import matplotlib as mpl
	import matplotlib.pyplot as plt
	C=Candidato.objects.filter(inscrito=False)
	especificos=list(C.values_list('D_especificos',flat=True))
	especificos=[i for i in especificos if i !='']
	W=' '.join(especificos)
	W=W.replace('de', '').replace('Antecedente', '').replace('en', '')
	wordcloud = WordCloud(
                          background_color='white',
                          max_words=200,
                          max_font_size=40, 
                          width=400, height=250,
                          random_state=42
                         ).generate(W)
	plt.figure(figsize=(8,6))    
	plt.imshow(wordcloud)
	plt.axis('off')
	media=settings.MEDIA_ROOT
	plt.savefig(os.path.join(media,'wordcloud_D_Especifico.png'),dpi=1500)
    

	return os.path.join("/media/",'wordcloud_D_Especifico.png')

def demografico_continuo():
	C=Candidato.objects.filter(inscrito=True)
	edad=C.values_list('edad',flat=True)
	peso=[c.ingreso.peso if hasattr(c,'ingreso') else None for c in C]
	estatura=[c.ingreso.estatura if hasattr(c,'ingreso') else None for c in C]

	T=pd.DataFrame(list(zip(edad,peso,estatura)),columns=['edad','peso','estatura'])
	continuo_values=list(T.edad.values)+list(T.peso.values)+list(T.estatura.values)
	continuo_variable=["Edad"]*len(T)+["Peso (Kgs)"]*len(T)+["Estatura (cms)"]*len(T)
	continuo=pd.DataFrame([continuo_values,continuo_variable],index=['valor','Variable']).T
	fig = px.violin(continuo,y='valor',color='Variable',box=True,points='all')
	plot_div = plot(fig, output_type='div',filename='demografico_continuo')

	return plot_div

def demografico_categorical():
	C=Candidato.objects.filter(inscrito=True)
	sexo=[c.sexo for c in C]
	lateralidad=[c.ingreso.lateralidad if hasattr(c,'ingreso') else None for c in C]
	nivel_educativo=[c.ingreso.n_educativo if hasattr(c,'ingreso') else None for c in C]

	T=pd.DataFrame(list(zip(sexo,lateralidad,nivel_educativo)),columns=['sexo','lateralidad','nivel_educativo'])
	categorical_values=list(T.sexo.values)+list(T.lateralidad.values)+list(T.nivel_educativo.values)
	categorical_variable=["Sexo"]*len(T)+["Lateralidad"]*len(T)+["Nivel Educativo"]*len(T)
	categorical=pd.DataFrame([categorical_values,categorical_variable],index=['valor','Variable']).T
	fig = px.histogram(categorical,x='valor',color='Variable')
	
	plot_div = plot(fig, output_type='div',filename='demografico_categorical')

	return plot_div

def demografico_map():
	municipio=pd.read_csv("/home/colciencias/SanJose/apps/graphs/municipioscolombia.csv",index_col='ciudad')
	inscrito=Candidato.objects.filter(inscrito=True)  
	nacimiento=[c.ingreso.lugar_nacimiento if hasattr(c,'ingreso') else None for c in inscrito]
	residencia=[c.ingreso.lugar_residencia if hasattr(c,'ingreso') else None for c in inscrito]
	ciudades=[i.split(', ')[-1] for i in list(nacimiento)]+[i.split(', ')[-1] for i in list(residencia)]
	lugar=['Nacimiento']*len(nacimiento)+['Residencia']*len(residencia)
	A=pd.DataFrame([ciudades,lugar],index=['Ciudad','Lugar']).T
	filter_c=municipio.loc[A.Ciudad].reset_index()
	filter_c['Lugar']=A.Lugar
	X=filter_c.groupby(filter_c.columns.tolist(),as_index=False).size().reset_index().rename(columns={0:'Frecuencia'})
	px.set_mapbox_access_token("pk.eyJ1IjoiY3B1bGlkbzk0IiwiYSI6ImNqejNxMXFoaTA0MzgzY3MxOHVnZTkwcGMifQ.-dGFAmjoYPK9kXWSrAbBqg")
	fig = px.scatter_mapbox(X, lat="latitude", lon="longitude",hover_data=['ciudad','departamento'],zoom=4,color='Lugar',size='Frecuencia')
	plot_div = plot(fig, output_type='div',filename='demografico_map')

	return plot_div


def demografico_multi_scatter():
	C=Candidato.objects.filter(inscrito=True)
	edad=C.values_list('edad',flat=True)
	peso=[c.ingreso.peso if hasattr(c,'ingreso') else None for c in C]
	estatura=[c.ingreso.estatura if hasattr(c,'ingreso') else None for c in C]
	sexo=[c.sexo for c in C]
	lateralidad=[c.ingreso.lateralidad if hasattr(c,'ingreso') else None for c in C]
	nivel_educativo=[c.ingreso.n_educativo if hasattr(c,'ingreso') else None for c in C]
	T=pd.DataFrame(list(zip(edad,peso,estatura,sexo,lateralidad,nivel_educativo)),columns=['Edad','Peso (Kgs)','Estatura (cms)','Sexo','Lateralidad','Nivel Educativo'])
	fig = px.scatter(T,x='Estatura (cms)',y='Peso (Kgs)',color='Sexo',size='Edad',facet_col='Nivel Educativo',
  								 marginal_x='box',marginal_y='box')
	plot_div = plot(fig, output_type='div',filename='demografico_multi_scatter')
	return plot_div


def demografico_multi_categorical():
  C=Candidato.objects.filter(inscrito=True)
  edad=C.values_list('edad',flat=True)
  peso=[c.ingreso.peso if hasattr(c,'ingreso') else None for c in C]
  estatura=[c.ingreso.estatura if hasattr(c,'ingreso') else None for c in C]
  sexo=[c.sexo for c in C]
  lateralidad=[c.ingreso.lateralidad if hasattr(c,'ingreso') else None for c in C]
  nivel_educativo=[c.ingreso.n_educativo if hasattr(c,'ingreso') else None for c in C]
  T=pd.DataFrame(list(zip(edad,peso,estatura,sexo,lateralidad,nivel_educativo)),columns=['Edad','Peso (Kgs)','Estatura (cms)','Sexo','Lateralidad','Nivel Educativo'])


  fig = px.parallel_categories(T,color='Edad')

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
  fig['layout'].update(legend=dict(orientation="h"))  

  plot_div = plot(fig, output_type='div',filename='clinica_grupod')
  return plot_div

def clinica_conciencia():
  C=Candidato.objects.filter(inscrito=True)
  conciencia=[c.ingreso.conciencia if hasattr(c,'ingreso') else None for c in C]

  labels,values=np.unique(conciencia,return_counts=True)

  fig = go.Figure(data=[go.Pie(labels=labels,
                             	 values=values,
                               hole=0.3,
                               text=labels,
                               hoverinfo='text+value'
                            	)
  											] 
  								)
  fig['layout'].update(legend=dict(orientation="h"))  

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
    
	fig['layout'].update(legend=dict(orientation="h"))
	plot_div = plot(fig, output_type='div',filename='clinica_a_patologicos')

	return plot_div

def clinica_antecedentes():
	from django.conf import settings
	from wordcloud import WordCloud
	import matplotlib as mpl
	import matplotlib.pyplot as plt
	from apps.paciente.models import Ingreso    
	I=Ingreso.objects.all()
	antecedentes = ['a_patologicos_cual','a_toxico_alergenicos','a_familiares']
	for i in antecedentes:
		W=" ".join([i for i in list(I.values_list(i,flat=True)) if i])
		wordcloud = WordCloud(
                              background_color='white',
                              max_words=200,
                              max_font_size=40, 
                              width=400, height=250,
                              random_state=42
                             ).generate(W)
		plt.figure(figsize=(8,6))    
		plt.imshow(wordcloud)
		plt.axis('off')
		media=settings.MEDIA_ROOT
		plt.savefig(os.path.join(media,'wordcloud_'+i+'.png'),dpi=1500)
    

	return [os.path.join("/media/",'wordcloud_'+i+'.png') for i in antecedentes]





def clinica_uci_g():
  C=Candidato.objects.filter(inscrito=True)
  glasgow= [c.uci.glasgowtotal if hasattr(c,'uci') else None for c in C]
  A=pd.DataFrame(glasgow,columns=['Glasgow Total Ingreso'])
  fig = px.box(A,y='Glasgow Total Ingreso')


  plot_div = plot(fig, output_type='div',filename='clinica_uci_g')
  return plot_div

def clinica_uci_egreso():
  C=Candidato.objects.filter(inscrito=True)
  egreso= [c.uci.condicion_egreso if hasattr(c,'uci') else None for c in C]
  A=pd.DataFrame(egreso,columns=['Condición de Egreso']).dropna()
  fig = px.histogram(A,x='Condición de Egreso')


  plot_div = plot(fig, output_type='div',filename='clinica_uci_egreso')
  return plot_div

def clinica_formularios():
  C=Candidato.objects.filter(inscrito=True)
  x=np.sum([len(c.get_neuro())>0 for c in C])*['Neurología']+\
  	np.sum([1 if hasattr(c,'informante') else 0 for c in C])*['Neuropsicología Informante']+\
  	np.sum([len(c.moca_set.all())>0 for c in C])*['Moca']+\
  	np.sum([1 if hasattr(c,'neuropsi') else 0 for c in C])*['Neuropsi']+\
  	np.sum([1 if hasattr(c,'lectura_resonancia') else 0 for c in C])*['Lectura Estructural']

  fig = go.Figure(data=[go.Histogram(x=x)])
  fig['layout'].update(legend=dict(orientation="h"))

  plot_div = plot(fig, output_type='div',filename='clinica_formularios')
  return plot_div

def uci_glasgow_ingreso():
    from apps.paciente.models import Uci
    U=Uci.objects.filter(candidato__inscrito=True)
    variables=[['Apertura ocular','apertura_ocular'],['Respuesta motora','respuesta_motora'],['Respuesta Verbal','respuesta_verbal'],['Glasgow Total ingreso','glasgowtotal']]
    
    A=pd.DataFrame()
    for i in variables:
        A[i[0]]=U.values_list(i[1],flat=True)
        
    fig=px.parallel_categories(A,dimensions=[v[0] for v in variables])#,color='Glasgow Total ingreso')
    
    plot_div = plot(fig, output_type='div',filename='uci_glasgow_ingreso')
    return plot_div

def uci_variables_vs_egreso():
    from apps.paciente.models import Uci
    U=Uci.objects.filter(candidato__inscrito=True)
    variables=[['fallaorganica','Falla Organica'],['sepsis','Sepsis'],['presion_intracraneana','Presión Intracraneana'],['monitoria_pic','Monitoria Pic'],['ventilacionmecanica','Ventilación Mecanica'],['soportevasopresor','Soporte Vasopresor'],['condicion_egreso','Condición Egreso']]
    
    A=pd.DataFrame()
    for i in variables:
        A[i[1]]=U.values_list(i[0],flat=True)
        
    fig=px.parallel_categories(A,dimensions=[v[1] for v in variables])
    
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
    
	fig['layout'].update(legend=dict(orientation="h"))
	plot_div = plot(fig, output_type='div',filename='uci_falla_organica')

	return plot_div

def uci_glasgow_egreso():
    from apps.paciente.models import Uci
    U=Uci.objects.filter(candidato__inscrito=True)
    variables=[['Apertura ocular','apertura_ocular_e'],['Respuesta motora','respuesta_motora_e'],['Respuesta Verbal','respuesta_verbal_e'],['Glasgow Total Egreso','glasgowtotal_e']]
    
    A=pd.DataFrame()
    for i in variables:
        A[i[0]]=U.values_list(i[1],flat=True)
        
    fig=px.parallel_categories(A,dimensions=[v[0] for v in variables])#,color='Glasgow Total ingreso')
    
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
    
	fig['layout'].update(legend=dict(orientation="h"))
	plot_div = plot(fig, output_type='div',filename='uci_causa_mortalidad')

	return plot_div

def uci_dx_egreso():
	from django.conf import settings
	from wordcloud import WordCloud
	import matplotlib as mpl
	import matplotlib.pyplot as plt
	from apps.paciente.models import Uci   
	U=Uci.objects.filter(candidato__inscrito=True)


	W=" ".join([i for i in list(U.values_list('dx_egreso',flat=True)) if i])
	wordcloud = WordCloud(
                              background_color='white',
                              max_words=200,
                              max_font_size=40, 
                              width=400, height=250,
                              random_state=42
                             ).generate(W)
	plt.figure(figsize=(8,6))    
	plt.imshow(wordcloud)
	plt.axis('off')
	media=settings.MEDIA_ROOT
	plt.savefig(os.path.join(media,'wordcloud_uci_dx_egreso.png'),dpi=1500)
    

	return os.path.join("/media/",'wordcloud_uci_dx_egreso.png')





def neuropsi_vs_G_diagnostico():
  from apps.paciente.models import Neuropsi
  N=Neuropsi.objects.all()

  A=pd.DataFrame([[n.candidato.G_diagnostico,n.orientacion,n.atencion,n.codificacion,n.evocacion] for n in N], 
  	columns=['Grupo Diagnóstico','Orientación','Atención','Codificación','Evocación']).dropna()
  fig=px.strip(A,x='Atención',y='Orientación',facet_col='Codificación',facet_row='Evocación',
    color='Grupo Diagnóstico',
    
     category_orders={'Orientación':['Normal Alto','Normal','Moderado','Severo'],
                      'Atención':['Normal Alto','Normal','Moderado','Severo'],
                      'Codificación':['Normal Alto','Normal','Moderado','Severo'],
                      'Evocación':['Normal Alto','Normal','Moderado','Severo']
                     })


  plot_div = plot(fig, output_type='div',filename='neuropsi_vs_G_diagnostico')
  return plot_div

def neuropsi_vs_G_diagnostico_2():
  from apps.paciente.models import Neuropsi
  N=Neuropsi.objects.all()

  A=pd.DataFrame([[n.candidato.G_diagnostico,n.orientacion,n.atencion,n.codificacion,n.evocacion] for n in N], 
  	columns=['Grupo Diagnóstico','Orientación','Atención','Codificación','Evocación']).dropna()
  fig=px.parallel_categories(A)


  plot_div = plot(fig, output_type='div',filename='neuropsi_vs_G_diagnostico_2')
  return plot_div

