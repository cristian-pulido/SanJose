from plotly.offline import plot
from plotly.subplots import  make_subplots
import plotly.graph_objs as go 
import pandas as pd 
from datetime import datetime
import requests
from apps.paciente.models import Candidato
import numpy as np
import plotly.express as px



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

def demografico_continuo():
	C=Candidato.objects.filter(inscrito=True)
	edad=C.values_list('edad',flat=True)
	peso=[c.ingreso.peso if hasattr(c,'ingreso') else None for c in C]
	estatura=[c.ingreso.estatura if hasattr(c,'ingreso') else None for c in C]

	T=pd.DataFrame(list(zip(edad,peso,estatura)),columns=['edad','peso','estatura'])
	continuo_values=list(T.edad.values)+list(T.peso.values)+list(T.estatura.values)
	continuo_variable=["Edad"]*len(T)+["Peso (Kgs)"]*len(T)+["Estatura (cms)"]*len(T)
	continuo=pd.DataFrame([continuo_values,continuo_variable],index=['valor','Variable']).T
	fig = px.box(continuo,y='valor',color='Variable')
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



