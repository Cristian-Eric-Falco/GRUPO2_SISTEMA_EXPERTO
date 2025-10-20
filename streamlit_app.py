import collections
import collections.abc
collections.Mapping = collections.abc.Mapping
import streamlit as st
from engine import BodyTypeEngine
import graphviz

st.set_page_config(
    page_title="Clasificador de Somatotipos", 
    page_icon="🏋️", 
    layout="centered"
)

# --- Título principal  ---
st.markdown(
    "<h1 style='text-align: center; color: #3498db;'>Clasificador de Somatotipos</h1>", 
    unsafe_allow_html=True
)


st.divider()

# --- Texto de bienvenida ---
st.markdown(
    "<p style='text-align: center; font-size: 1.1em;'>Introduce tus medidas en el panel de la izquierda para comenzar.</p>", 
    unsafe_allow_html=True
)


with st.sidebar:
    st.header("Introduce tus datos 📝")


    with st.form("input_form"):
        # CORREGIDO: Restauramos los parámetros numéricos
        peso = st.number_input(
            "Peso (kg)",
            min_value=20.0,
            max_value=250.0,
            value=70.0,
            step=0.5
        )
        masa_muscular = st.number_input(
            "Masa muscular estimada (%)",
            min_value=5.0,
            max_value=60.0,
            value=32.0,
            step=0.5
        )
        grasa = st.number_input(
            "Nivel de grasa corporal estimado (%)",
            min_value=3.0,
            max_value=60.0,
            value=18.0,
            step=0.5
        )

        submitted = st.form_submit_button("Evaluar")

    with st.expander("ℹ️ Sobre este Proyecto"):
        st.markdown("""
        Este es un sistema experto simple que utiliza la librería `experta` de Python.
        Clasifica el somatotipo basándose en un conjunto de reglas
        predefinidas sobre el peso, la grasa y la masa muscular.
        """)

    with st.expander("⚠️ Limitaciones del Modelo"):
        st.markdown("""
        Este modelo es una **simplificación académica**.
        * **No considera:** Edad, sexo, altura, o genética.
        * **Reglas Fijas:** Las reglas son fijas
            y no se adaptan al individuo.
        * **No es consejo médico:** Los resultados son solo
            orientativos y no reemplazan a una evaluación profesional.
        """)



if submitted:
    engine = BodyTypeEngine()
    tipo, trace_mensajes, trace_claves = engine.classify(peso=peso, masa_muscular=masa_muscular, grasa=grasa)

    tab_resultado, tab_explicacion, tab_arbol = st.tabs(
        ["📊 Resultado Principal", "👣 Explicación Paso a Paso", "🌳 Árbol de Inferencia"]
    )

    # --- Pestaña 1: Resultado, Foto y Consejos ---
    with tab_resultado:

        # --- Primer Contenedor: El Texto del Resultado ---
        with st.container(border=True):
            st.subheader("Resultado de la Clasificación")

            if tipo == 'ectomorfo':
                st.success("Resultado: Ectomorfo")
            elif tipo == 'mesomorfo':
                st.success("Resultado: Mesomorfo")
            elif tipo == 'endomorfo':
                st.success("Resultado: Endomorfo")
            else:
                st.info("Resultado: Indeterminado")

        # --- Segundo Contenedor: La Imagen ---
        # (Este bloque ahora está CORRECTAMENTE indentado dentro de 'with tab_resultado:')
        with st.container(border=True):
            st.markdown("<h3 style='text-align: center;'>Visualización</h3>", unsafe_allow_html=True)
            
            ruta_base = "imagenes/" 
            
            col1, col2, col3 = st.columns([1.3, 1, 1.3])
            with col2:
                if tipo in ['ectomorfo', 'mesomorfo', 'endomorfo']:
                    st.image(ruta_base + f"{tipo}.jpg", use_container_width=True)

        # --- Tercer Contenedor: Recomendaciones ---
        # (Este bloque ahora está CORRECTAMENTE indentado dentro de 'with tab_resultado:')
        with st.expander("Ver recomendaciones de entrenamiento y nutrición 🏋️‍♂️"):
            if tipo == 'ectomorfo':
                st.markdown("""
                **Objetivo Principal:** Ganar masa muscular.
                * **Entrenamiento:** Enfócate en la fuerza y la hipertrofia. Usa ejercicios compuestos (sentadillas, peso muerto, press de banca). Descansa más entre series (2-3 min). Limita el cardio.
                * **Nutrición:** Un superávit calórico es esencial. Prioriza carbohidratos complejos (avena, arroz, patata) y proteínas (1.8g-2.2g por kg de peso). No le temas a las grasas saludables.
                """)

            elif tipo == 'mesomorfo':
                st.markdown("""
                **Objetivo Principal:** Ganancia muscular limpia o recomposición.
                * **Entrenamiento:** Una mezcla de fuerza (rangos de 5-8 repeticiones) e hipertrofia (8-15 repeticiones) es ideal. Puedes incluir más variedad y cardio moderado.
                * **Nutrición:** Mantén un ligero superávit calórico o calorías de mantenimiento. Controla las porciones y enfócate en comida de calidad. Una dieta balanceada (40% carbos, 30% prot, 30% grasas) suele funcionar bien.
                """)

            elif tipo == 'endomorfo':
                st.markdown("""
                **Objetivo Principal:** Pérdida de grasa y mantenimiento muscular.
                * **Entrenamiento:** La consistencia es clave. Aumenta tu NEAT (actividad diaria). El entrenamiento de fuerza es **fundamental** para mantener el músculo mientras pierdes grasa. Añade 2-3 sesiones de cardio (HIIT o LISS) por semana.
                * **Nutrición:** Necesitas un déficit calórico controlado. Eres más sensible a los carbohidratos; considera consumirlos cerca de tus entrenamientos. Prioriza la proteína alta (para saciedad y mantener músculo) y vegetales.
                """)

    # --- Pestaña 2: Explicación ---
    with tab_explicacion:
        st.subheader("Lógica de la Decisión")
        for i, t in enumerate(trace_mensajes, 1):
            st.write(f"{i}. {t}")

    # --- Pestaña 3: Árbol de Inferencia ---
    with tab_arbol:
        st.subheader("Camino de Inferencia")
        
        # (Aquí va todo tu código de 'import graphviz' y 'dot = ...')
        # (Asegúrate de que esté indentado dentro de 'with tab_arbol:')
        import graphviz
        trace = trace_claves
        dot = graphviz.Digraph(comment='Árbol de inferencia', graph_attr={'rankdir': 'TB', 'bgcolor': 'black', 'fontcolor': 'white'}, node_attr={'fontcolor': 'white', 'color': 'white'}, edge_attr={'color': 'white'})
        
        # (...el resto de tu código de graphviz...)
        
        dot.attr(label="Árbol de inferencia", labelloc='t', fontsize='24')

        # Definiciones de Nodos
        nodes_def = {
            "start": {"label": "Inicio", "shape": "circle", "style": "filled", "fillcolor": "gray"},
            "masa_baja": {"label": "Masa < 30"},
            "masa_alta": {"label": "Masa ≥ 30"},
            "grasa_baja": {"label": "Grasa < 15"},
            "grasa_media": {"label": "Grasa 15–17.9"},
            "grasa_alta": {"label": "Grasa ≥ 18"},
            "peso_bajo": {"label": "Peso < 60"},
            "peso_medio": {"label": "Peso 60–90"},
            "peso_alto": {"label": "Peso > 90"},
            "ecto": {"label": "ECTOMORFO", "style": "filled", "fillcolor": "white"},
            "meso": {"label": "MESOMORFO", "style": "filled", "fillcolor": "white"},
            "endo": {"label": "ENDOMORFO", "style": "filled", "fillcolor": "white"}
        }

        # Aplicar colores iniciales o de traza
        for key, attrs in nodes_def.items():
            if key in trace:
                attrs['fillcolor'] = "red"
                attrs['style'] = "filled"
                if key == "start":
                    attrs['fillcolor'] = "gray"
            elif key in ["ecto", "meso", "endo"]:
                if key in trace:
                    attrs['fillcolor'] = "red"
                    attrs['style'] = "filled"
                else:
                    attrs['fillcolor'] = "white"
                    attrs['color'] = "white"
            elif key == "start":
                attrs['fillcolor'] = "gray"
            else:
                attrs.pop('style', None)
                attrs.pop('fillcolor', None)
                attrs['color'] = "white"
            dot.node(key, **attrs)

        # Conexiones Jerárquicas y coloreo
        dot.edge("start", "masa_baja", color="red" if "masa_baja" in trace else "white")
        dot.edge("start", "masa_alta", color="red" if "masa_alta" in trace else "white")

        masa_nodes = ["masa_baja", "masa_alta"]
        grasa_nodes = ["grasa_baja", "grasa_media", "grasa_alta"]
        peso_nodes = ["peso_bajo", "peso_medio", "peso_alto"]

        for m in masa_nodes:
            for g in grasa_nodes:
                edge_color = "red" if m in trace and g in trace else "white"
                dot.edge(m, g, color=edge_color)

        for g in grasa_nodes:
            for p in peso_nodes:
                edge_color = "red" if g in trace and p in trace else "white"
                dot.edge(g, p, color=edge_color)

        # Definición del diccionario 'combinaciones'
        combinaciones = {
            "ecto": [
                ("masa_baja", "grasa_baja", "peso_bajo"),("masa_baja", "grasa_baja", "peso_medio"),
                ("masa_baja", "grasa_baja", "peso_alto"),("masa_baja", "grasa_media", "peso_bajo"),
                ("masa_baja", "grasa_media", "peso_medio"),
            ],
            "meso": [
                ("masa_alta", "grasa_baja", "peso_bajo"),("masa_alta", "grasa_baja", "peso_medio"),
                ("masa_alta", "grasa_baja", "peso_alto"),("masa_alta", "grasa_media", "peso_bajo"),
                ("masa_alta", "grasa_media", "peso_medio"),
            ],
            "endo": [
                ("masa_baja", "grasa_media", "peso_alto"),("masa_baja", "grasa_alta", "peso_bajo"),
                ("masa_baja", "grasa_alta", "peso_medio"),("masa_baja", "grasa_alta", "peso_alto"),
                ("masa_alta", "grasa_media", "peso_alto"),("masa_alta", "grasa_alta", "peso_bajo"),
                ("masa_alta", "grasa_alta", "peso_medio"),("masa_alta", "grasa_alta", "peso_alto"),
            ]
        }

        # Conexiones Finales
        final_connections = {}
        for tipo_final, rutas in combinaciones.items():
            for (m, g, p) in rutas:
                if p not in final_connections:
                    final_connections[p] = set()
                final_connections[p].add(tipo_final)

        for p_node, tipos in final_connections.items():
            for tipo_node in tipos:
                edge_color = "red" if p_node in trace and tipo_node in trace else "white"
                dot.edge(p_node, tipo_node, color=edge_color)

        st.graphviz_chart(dot)










