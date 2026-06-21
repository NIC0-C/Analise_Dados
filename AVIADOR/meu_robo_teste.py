import cv2
import mss
import numpy as np
import pytesseract
import time

pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

regiao_ultimo_resultado = {"top": 182, "left": 290, "width": 60, "height": 28}
regiao_centro = {"top": 365, "left": 535, "width": 240, "height": 95}

historico_resultados = []
ultimo_resultado_salvo = ""

with mss.mss() as sct:
    cv2.namedWindow("Visualizacao - Centro", cv2.WINDOW_AUTOSIZE)
    cv2.namedWindow("Visualizacao - Ultimo Jogo", cv2.WINDOW_AUTOSIZE)
    
    cv2.setWindowProperty("Visualizacao - Centro", cv2.WND_PROP_TOPMOST, 1)
    cv2.setWindowProperty("Visualizacao - Ultimo Jogo", cv2.WND_PROP_TOPMOST, 1)

    print("🤖 Robô Ativo! Monitore as duas pequenas janelas na tela.\n")

    while True:
        print_centro = sct.grab(regiao_centro)
        img_centro = cv2.cvtColor(np.array(print_centro), cv2.COLOR_BGRA2GRAY)
        
        print_ultimo = sct.grab(regiao_ultimo_resultado)
        img_ultimo = cv2.cvtColor(np.array(print_ultimo), cv2.COLOR_BGRA2GRAY)
        
        config_numeros = r"--psm 6 -c tessedit_char_whitelist=0123456789."
        
        txt_centro = pytesseract.image_to_string(img_centro, config=config_numeros).strip()
        txt_ultimo = pytesseract.image_to_string(img_ultimo, config=config_numeros).strip()
        
        if txt_centro:
            print(f"[Multiplicador Atual]: {txt_centro}x")
            
        if txt_ultimo and txt_ultimo != ultimo_resultado_salvo:
            try:
                valor_float = float(txt_ultimo)
                ultimo_resultado_salvo = txt_ultimo
                historico_resultados.append(valor_float)
                
                if len(historico_resultados) > 5:
                    historico_resultados.pop(0)
                    
                print("\n" + "="*40)
                print(f"🏁 NOVA RODADA DETECTADA NO HISTÓRICO!")
                print(f"📋 Seus últimos jogos salvos: {historico_resultados}")
                
                if len(historico_resultados) >= 3:
                    if historico_resultados[-1] < 1.50 and historico_resultados[-2] < 1.50 and historico_resultados[-3] < 1.50:
                        print("🚨 PADRÃO DETECTADO: 3 baixos seguidos!")
                        print("🔮 PREVISÃO: Alta chance de vir um número MAIOR que 2.00x na próxima!")
                    else:
                        print("⏳ Aguardando padrão de 3 números baixos...")
                print("="*40 + "\n")
                
            except ValueError:
                pass
            
        cv2.imshow("Visualizacao - Centro", img_centro)
        cv2.imshow("Visualizacao - Ultimo Jogo", img_ultimo)
        
        if cv2.waitKey(200) & 0xFF == ord("q"):
            break

cv2.destroyAllWindows()