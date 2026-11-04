"""Interfaz de chat. Arranque: streamlit run ui/streamlit_app.py"""
import os

import httpx
import streamlit as st

API_URL = os.getenv("API_URL", "http://localhost:8000")

st.set_page_config(page_title="Asistente de la Distribuidora", page_icon="📦")
st.title("📦 Asistente de la Distribuidora")
st.caption("Pregunta por datos (ventas, inventario) o por documentos (contratos, políticas).")

if "historial" not in st.session_state:
    st.session_state.historial = []

for m in st.session_state.historial:
    with st.chat_message(m["role"]):
        st.markdown(m["content"])
        if m.get("detalle"):
            with st.expander("Cómo lo respondí"):
                st.json(m["detalle"])

if pregunta := st.chat_input("Escribe tu pregunta…"):
    st.session_state.historial.append({"role": "user", "content": pregunta})
    with st.chat_message("user"):
        st.markdown(pregunta)
    with st.chat_message("assistant"):
        with st.spinner("Pensando… (un modelo local en laptop tarda unos segundos)"):
            try:
                r = httpx.post(f"{API_URL}/chat", json={"pregunta": pregunta}, timeout=300).json()
                texto = r.get("respuesta") or f"Error: {r.get('detail')}"
                detalle = {k: r.get(k) for k in ("ruta", "sql", "fuentes")}
            except Exception as e:
                texto, detalle = f"No pude conectar con la API: {e}", None
        st.markdown(texto)
        if detalle:
            with st.expander("Cómo lo respondí"):
                st.json(detalle)
    st.session_state.historial.append({"role": "assistant", "content": texto, "detalle": detalle})
