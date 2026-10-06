# Mostra a IA jogando as fases definidas em config.FASES_DEMONSTRACAO numa janela do OpenCV.
# É chamado automaticamente ao final do treino, mas também pode ser rodado sozinho: python assistir.py
import os
import cv2
from stable_baselines3 import PPO
import config
from ambiente import criar_ambiente


def desenhar_tela(frame_rgb, fase, info):
	frame = cv2.cvtColor(frame_rgb, cv2.COLOR_RGB2BGR)  # o OpenCV trabalha com BGR
	altura, largura = frame.shape[:2]
	frame = cv2.resize(frame, (largura * config.ESCALA_JANELA, altura * config.ESCALA_JANELA), interpolation=cv2.INTER_NEAREST)
	texto = f"Fase {fase}   x: {info.get('x_pos', 0)}"
	cv2.putText(frame, texto, (10, frame.shape[0] - 15), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 255), 2)
	cv2.imshow("Mario PPO", frame)
	# waitKey controla a velocidade e processa os eventos da janela. Retorna a tecla apertada
	return cv2.waitKey(int(1000 / config.FPS_DEMONSTRACAO)) & 0xFF


def jogar_fase(modelo, fase):
	"""Joga uma tentativa da fase. Retorna True se o Mario pegou a bandeira, False se não pegou e None se o usuário apertou 'q'."""
	env = criar_ambiente(fase, render_mode="rgb_array")
	obs, info = env.reset()
	for _ in range(config.MAX_PASSOS_DEMONSTRACAO):
		acao, _ = modelo.predict(obs, deterministic=config.ACAO_DETERMINISTICA)
		obs, recompensa, terminado, truncado, info = env.step(int(acao))  # predict devolve um array numpy
		if desenhar_tela(env.render(), fase, info) == ord("q"):
			env.close()
			return None
		if terminado or truncado:
			break
	env.close()

	if info["flag_get"]:
		print(f"Fase {fase}: CONCLUÍDA!")
	else:
		print(f"Fase {fase}: não concluiu (chegou até x = {info['x_pos']})")
	cv2.waitKey(1500)  # pausa curta antes da próxima fase
	return info["flag_get"]


def mostrar_fases(modelo):
	print("Mostrando a IA jogando. Aperte 'q' na janela para sair.")
	for fase in config.FASES_DEMONSTRACAO:
		if jogar_fase(modelo, fase) is None:
			break
	cv2.destroyAllWindows()


if __name__ == "__main__":
	if not os.path.exists(config.ARQUIVO_MODELO + ".zip"):
		raise SystemExit("Nenhum modelo treinado encontrado. Rode primeiro: python treinar.py")
	mostrar_fases(PPO.load(config.ARQUIVO_MODELO))
