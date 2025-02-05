import streamlit as st
import time
import random

# Función para iniciar el juego
def start_game():
    # Iniciar las variables del juego
    st.session_state['started'] = True
    st.session_state['solved'] = False
    st.session_state['hints_used'] = 0
    st.session_state['puzzle_answer'] = random.randint(1, 100)  # Número aleatorio como respuesta
    st.session_state['timer'] = time.time()  # Iniciar temporizador
    st.session_state['time_left'] = 600  # 10 minutos para resolver el escape room (en segundos)
    st.session_state['game_over'] = False
    st.session_state['end_message'] = ""

# Función para verificar la respuesta del jugador
def check_answer(player_answer):
    correct_answer = st.session_state['puzzle_answer']
    if player_answer == correct_answer:
        st.session_state['solved'] = True
        st.session_state['end_message'] = "¡Felicidades! Has resuelto el puzzle y escapado."
    else:
        st.session_state['end_message'] = "Respuesta incorrecta. Intenta de nuevo."

# Función para mostrar la habitación inicial
def show_intro():
    st.title("Escape Room Virtual")
    st.write("¡Bienvenido al Escape Room Virtual!")
    st.write("Para escapar de la habitación, debes resolver el siguiente puzzle.")
    st.write("Tienes 10 minutos para hacerlo.")
    
    # Mostrar puzzle básico: un número aleatorio
    st.write("Adivina el número entre 1 y 100 que desbloquea la puerta.")
    
    # Mostrar cuadro de texto para la respuesta
    player_answer = st.number_input("Introduce tu respuesta (un número entre 1 y 100)", min_value=1, max_value=100)
    
    # Verificar la respuesta
    if player_answer:
        check_answer(player_answer)
    
    # Mostrar mensaje de resultado
    st.write(st.session_state['end_message'])

    # Mostrar el botón de reiniciar si el juego se resolvió o terminó
    if st.session_state['solved'] or st.session_state['game_over']:
        if st.button("Reiniciar Juego"):
            start_game()

# Función para mostrar temporizador y el tiempo restante
def show_timer():
    elapsed_time = time.time() - st.session_state['timer']
    time_left = max(0, st.session_state['time_left'] - elapsed_time)
    minutes = int(time_left // 60)
    seconds = int(time_left % 60)
    
    if time_left == 0:
        st.session_state['game_over'] = True
        st.session_state['end_message'] = "¡Se acabó el tiempo! No lograste escapar."

    st.write(f"Tiempo restante: {minutes:02}:{seconds:02}")

# Función para usar pistas
def use_hint():
    if st.session_state['hints_used'] < 3:
        st.session_state['hints_used'] += 1
        hint_message = f"Hint {st.session_state['hints_used']}: El número está entre {st.session_state['puzzle_answer'] - 10} y {st.session_state['puzzle_answer'] + 10}."
        st.write(hint_message)
    else:
        st.write("Has usado todas las pistas disponibles.")

# Interfaz de Streamlit
def main():
    # Si no se ha iniciado el juego, mostrar la introducción
    if 'started' not in st.session_state or not st.session_state['started']:
        start_game()

    if st.session_state['game_over']:
        st.write(st.session_state['end_message'])
        if st.button("Reiniciar Juego"):
            start_game()
    else:
        # Mostrar la habitación y los puzzles
        show_intro()
        show_timer()

        # Botón para usar pistas
        if st.button("Usar pista"):
            use_hint()

if __name__ == "__main__":
    main()
