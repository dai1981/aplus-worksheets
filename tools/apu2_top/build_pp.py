# -*- coding: utf-8 -*-
"""privacypolicy.html に de fr it es pt tr を 足す → out/privacypolicy.html"""
import os, re
HERE = os.path.dirname(os.path.abspath(__file__))
src = open(os.path.join(HERE, "en_privacy.html"), encoding="utf-8").read()
LINE = "https://line.me/ti/g2/bNMNEcyFfTX1-QEg9Jv48UjSb-_U2iFtuk_90g?utm_source=invitation&amp;utm_medium=link_copy&amp;utm_campaign=default"

P = {
 "de": dict(name="Deutsch", title="Datenschutzerklärung", back="Zurück", hl="de", upd="Erstellt am: 16. Oktober 2026",
  lead="aplus (apu2.com) ist eine kostenlose Lernseite, betrieben von Aplus Inc. (えいぷら Aplus). Hier erklären wir, welche Informationen wir nutzen und wofür.",
  s=[("1. Welche Informationen wir nutzen", ["Dein Lernverlauf und deine Einstellungen (Antworten, Fortschritt, Punkte). Sie werden in deinem Browser und mit einer zufälligen ID auf unserem Server gespeichert. Für die Nutzung brauchen wir weder Namen noch E-Mail-Adresse oder Anschrift.",
       "Zugriffsdaten wie aufgerufene Seiten, Gerät, Browser und ungefährer Standort, die Google Analytics mit Cookies erfasst.",
       "Cookies, die Google AdSense für die Anzeige von Werbung verwendet.", "Nachrichten, die du uns über LINE schickst."]),
     ("2. Wofür wir sie nutzen", ["Um deinen Lernstand zu speichern und passende Aufgaben zu zeigen.", "Um zu verstehen, wie die Seite genutzt wird, und sie zu verbessern.",
       "Um Werbung zu zeigen, damit die Seite kostenlos bleibt.", "Um deine Fragen zu beantworten."]),
     ("3. Dienste, die wir nutzen", ["Google Analytics (Google LLC): {ga}Wie Google Daten verwendet{/a}.",
       "Google AdSense (Google LLC): Google und seine Partner können Cookies verwenden, um Werbung auf Grundlage deiner Besuche auf dieser und anderen Websites zu zeigen. Personalisierte Werbung kannst du in den {ads}Google-Anzeigeneinstellungen{/a} ausschalten.",
       "LINE (LY Corporation): für unsere Community-Gruppe und für Anfragen."]),
     ("4. Weitergabe", ["Wir verkaufen deine Informationen nicht. Wir geben sie nicht an andere weiter, außer an die oben genannten Dienste oder wenn ein Gesetz es verlangt."]),
     ("5. Daten löschen", ["Nutze die Zurücksetzen-Taste auf jeder Seite oder lösche die Browserdaten. Wenn Daten auf unserem Server gelöscht werden sollen, schreib uns über LINE."]),
     ("6. Kinder", ["Wenn du jünger als 13 Jahre bist, nutze die Seite bitte zusammen mit deinen Eltern oder einer erziehungsberechtigten Person."]),
     ("7. Änderungen", ["Wir können diese Erklärung ändern. Die neue Fassung gilt, sobald sie auf dieser Seite steht."]),
     ("8. Kontakt", ["Bitte schreib uns über {line}LINE{/a}."])]),
 "fr": dict(name="Français", title="Politique de confidentialité", back="Retour", hl="fr", upd="Établie le : 16 octobre 2026",
  lead="aplus (apu2.com) est un site d’apprentissage gratuit géré par Aplus Inc. (えいぷら Aplus). Cette page explique quelles informations nous utilisons et pourquoi.",
  s=[("1. Informations utilisées", ["Ton historique d’apprentissage et tes réglages (réponses, progression, scores). Ils sont enregistrés dans ton navigateur et sur notre serveur avec un identifiant aléatoire. Nous ne demandons ni nom, ni e-mail, ni adresse pour utiliser le site.",
       "Les données de connexion, comme les pages vues, l’appareil, le navigateur et la région approximative, collectées par Google Analytics avec des cookies.",
       "Les cookies utilisés par Google AdSense pour afficher des publicités.", "Les messages que tu nous envoies sur LINE."]),
     ("2. Pourquoi nous les utilisons", ["Pour enregistrer ta progression et te proposer les bonnes questions.", "Pour comprendre comment le site est utilisé et l’améliorer.",
       "Pour afficher des publicités qui permettent au site de rester gratuit.", "Pour répondre à tes questions."]),
     ("3. Services utilisés", ["Google Analytics (Google LLC) : {ga}Comment Google utilise les données{/a}.",
       "Google AdSense (Google LLC) : Google et ses partenaires peuvent utiliser des cookies pour afficher des publicités selon tes visites sur ce site et d’autres sites. Tu peux désactiver les annonces personnalisées dans les {ads}paramètres des annonces Google{/a}.",
       "LINE (LY Corporation) : pour notre groupe communautaire et le contact."]),
     ("4. Partage", ["Nous ne vendons pas tes informations. Nous ne les transmettons à personne, sauf aux services ci-dessus ou si la loi l’exige."]),
     ("5. Supprimer tes données", ["Utilise le bouton de réinitialisation de chaque page ou efface les données du navigateur. Pour supprimer les données enregistrées sur notre serveur, contacte-nous sur LINE."]),
     ("6. Enfants", ["Si tu as moins de 13 ans, utilise le site avec un parent ou un tuteur."]),
     ("7. Modifications", ["Cette politique peut être mise à jour. La nouvelle version s’applique dès sa publication sur cette page."]),
     ("8. Contact", ["Contacte-nous sur {line}LINE{/a}."])]),
 "it": dict(name="Italiano", title="Informativa sulla privacy", back="Indietro", hl="it", upd="Redatta il: 16 ottobre 2026",
  lead="aplus (apu2.com) è un sito gratuito per imparare, gestito da Aplus Inc. (えいぷら Aplus). Questa pagina spiega quali informazioni usiamo e perché.",
  s=[("1. Informazioni che usiamo", ["La tua cronologia di studio e le tue impostazioni (risposte, progressi, punteggi). Sono salvate nel tuo browser e sul nostro server con un ID casuale. Per usare il sito non chiediamo nome, e-mail o indirizzo.",
       "Dati di accesso come pagine visitate, dispositivo, browser e posizione approssimativa, raccolti da Google Analytics tramite cookie.",
       "Cookie usati da Google AdSense per mostrare annunci.", "Messaggi che ci invii su LINE."]),
     ("2. Perché le usiamo", ["Per salvare i tuoi progressi e proporti le domande giuste.", "Per capire come viene usato il sito e migliorarlo.",
       "Per mostrare annunci che mantengono il sito gratuito.", "Per rispondere alle tue domande."]),
     ("3. Servizi che usiamo", ["Google Analytics (Google LLC): {ga}Come Google utilizza i dati{/a}.",
       "Google AdSense (Google LLC): Google e i suoi partner possono usare cookie per mostrare annunci in base alle tue visite a questo e ad altri siti. Puoi disattivare gli annunci personalizzati nelle {ads}Impostazioni annunci di Google{/a}.",
       "LINE (LY Corporation): per il nostro gruppo della community e per i contatti."]),
     ("4. Condivisione", ["Non vendiamo le tue informazioni e non le diamo ad altri, tranne ai servizi indicati sopra o quando lo richiede la legge."]),
     ("5. Cancellare i dati", ["Usa il pulsante di azzeramento in ogni pagina oppure cancella i dati del browser. Per cancellare i dati salvati sul nostro server, contattaci su LINE."]),
     ("6. Minori", ["Se hai meno di 13 anni, usa il sito insieme a un genitore o a un tutore."]),
     ("7. Modifiche", ["Possiamo aggiornare questa informativa. La nuova versione vale da quando viene pubblicata su questa pagina."]),
     ("8. Contatti", ["Contattaci su {line}LINE{/a}."])]),
 "es": dict(name="Español", title="Política de privacidad", back="Volver", hl="es", upd="Fecha de creación: 16 de octubre de 2026",
  lead="aplus (apu2.com) es un sitio gratuito para aprender idiomas y matemáticas, gestionado por Aplus Inc. (えいぷら Aplus). Esta página explica qué información usamos y para qué.",
  s=[("1. Información que usamos", ["Tu historial de estudio y tus ajustes (respuestas, progreso, puntuaciones). Se guardan en tu navegador y en nuestro servidor con un identificador aleatorio. Para usar el sitio no pedimos tu nombre, correo electrónico ni dirección.",
       "Datos de acceso como las páginas vistas, el dispositivo, el navegador y la ubicación aproximada, que Google Analytics recoge con cookies.",
       "Cookies que usa Google AdSense para mostrar anuncios.", "Mensajes que nos envías por LINE."]),
     ("2. Para qué la usamos", ["Para guardar tu progreso y mostrarte las preguntas adecuadas.", "Para entender cómo se usa el sitio y mejorarlo.",
       "Para mostrar anuncios que mantienen el sitio gratis.", "Para responder a tus preguntas."]),
     ("3. Servicios que usamos", ["Google Analytics (Google LLC): {ga}Cómo usa Google los datos{/a}.",
       "Google AdSense (Google LLC): Google y sus socios pueden usar cookies para mostrar anuncios según tus visitas a este y a otros sitios. Puedes desactivar los anuncios personalizados en la {ads}configuración de anuncios de Google{/a}.",
       "LINE (LY Corporation): para nuestro grupo de la comunidad y el contacto."]),
     ("4. Cesión", ["No vendemos tu información ni la cedemos a terceros, salvo a los servicios anteriores o cuando lo exija la ley."]),
     ("5. Borrar tus datos", ["Usa el botón de reinicio de cada página o borra los datos del navegador. Para borrar los datos guardados en nuestro servidor, escríbenos por LINE."]),
     ("6. Menores", ["Si tienes menos de 13 años, usa el sitio con tu madre, tu padre o tu tutor."]),
     ("7. Cambios", ["Podemos actualizar esta política. La nueva versión se aplica desde que se publica en esta página."]),
     ("8. Contacto", ["Escríbenos por {line}LINE{/a}."])]),
 "pt": dict(name="Português", title="Política de privacidade", back="Voltar", hl="pt-BR", upd="Data de criação: 16 de outubro de 2026",
  lead="O aplus (apu2.com) é um site gratuito para aprender, mantido pela Aplus Inc. (えいぷら Aplus). Esta página explica quais informações usamos e por quê.",
  s=[("1. Informações que usamos", ["Seu histórico de estudo e suas configurações (respostas, progresso, pontuações). Eles ficam salvos no seu navegador e no nosso servidor com um ID aleatório. Para usar o site, não pedimos nome, e-mail nem endereço.",
       "Dados de acesso, como páginas vistas, dispositivo, navegador e localização aproximada, coletados pelo Google Analytics com cookies.",
       "Cookies usados pelo Google AdSense para mostrar anúncios.", "Mensagens que você nos envia pelo LINE."]),
     ("2. Por que usamos", ["Para salvar seu progresso e mostrar as questões certas.", "Para entender como o site é usado e melhorá-lo.",
       "Para mostrar anúncios que mantêm o site gratuito.", "Para responder às suas perguntas."]),
     ("3. Serviços que usamos", ["Google Analytics (Google LLC): {ga}Como o Google usa os dados{/a}.",
       "Google AdSense (Google LLC): o Google e seus parceiros podem usar cookies para mostrar anúncios com base nas suas visitas a este e a outros sites. Você pode desativar os anúncios personalizados nas {ads}configurações de anúncios do Google{/a}.",
       "LINE (LY Corporation): usado para o nosso grupo da comunidade e para contato."]),
     ("4. Compartilhamento", ["Não vendemos suas informações nem as repassamos a terceiros, exceto aos serviços acima ou quando a lei exigir."]),
     ("5. Apagar seus dados", ["Use o botão de reiniciar em cada página ou apague os dados do navegador. Para apagar os dados salvos no nosso servidor, fale com a gente pelo LINE."]),
     ("6. Crianças", ["Se você tem menos de 13 anos, use o site junto com seus pais ou responsáveis."]),
     ("7. Alterações", ["Podemos atualizar esta política. A nova versão vale a partir do momento em que for publicada nesta página."]),
     ("8. Contato", ["Fale com a gente pelo {line}LINE{/a}."])]),
 "tr": dict(name="Türkçe", title="Gizlilik politikası", back="Geri", hl="tr", upd="Oluşturulma tarihi: 16 Ekim 2026",
  lead="aplus (apu2.com), Aplus Inc. (えいぷら Aplus) tarafından işletilen ücretsiz bir öğrenme sitesidir. Bu sayfada hangi bilgileri neden kullandığımızı açıklıyoruz.",
  s=[("1. Kullandığımız bilgiler", ["Öğrenme geçmişin ve ayarların (cevaplar, ilerleme, puanlar). Bunlar tarayıcında ve rastgele bir kimlikle sunucumuzda saklanır. Siteyi kullanmak için adını, e-posta adresini ya da adresini istemiyoruz.",
       "Google Analytics’in çerezlerle topladığı, görüntülenen sayfalar, cihaz, tarayıcı ve yaklaşık konum gibi erişim verileri.",
       "Google AdSense’in reklam göstermek için kullandığı çerezler.", "LINE üzerinden bize gönderdiğin mesajlar."]),
     ("2. Neden kullanıyoruz", ["İlerlemeni kaydetmek ve sana uygun soruları göstermek için.", "Sitenin nasıl kullanıldığını anlamak ve geliştirmek için.",
       "Sitenin ücretsiz kalmasını sağlayan reklamları göstermek için.", "Sorularını cevaplamak için."]),
     ("3. Kullandığımız hizmetler", ["Google Analytics (Google LLC): {ga}Google verileri nasıl kullanır{/a}.",
       "Google AdSense (Google LLC): Google ve iş ortakları, bu siteye ve başka sitelere yaptığın ziyaretlere göre reklam göstermek için çerez kullanabilir. Kişiselleştirilmiş reklamları {ads}Google Reklam Ayarları{/a} sayfasından kapatabilirsin.",
       "LINE (LY Corporation): topluluk grubumuz ve iletişim için."]),
     ("4. Paylaşım", ["Bilgilerini satmayız. Yukarıdaki hizmetler ve yasaların gerektirdiği durumlar dışında kimseyle paylaşmayız."]),
     ("5. Verilerini silme", ["Her sayfadaki sıfırlama düğmesini kullanabilir ya da tarayıcı verilerini silebilirsin. Sunucumuzdaki verilerin silinmesi için bize LINE üzerinden yaz."]),
     ("6. Çocuklar", ["13 yaşından küçüksen siteyi annen, baban ya da velinle birlikte kullan."]),
     ("7. Değişiklikler", ["Bu politikayı güncelleyebiliriz. Yeni sürüm bu sayfada yayımlandığı andan itibaren geçerlidir."]),
     ("8. İletişim", ["Lütfen bize {line}LINE{/a} üzerinden yaz."])]),
}


def link(s, hl):
    s = s.replace("{ga}", '<a href="https://policies.google.com/technologies/partner-sites?hl=%s" target="_blank" rel="noopener">' % hl)
    s = s.replace("{ads}", '<a href="https://adssettings.google.com/" target="_blank" rel="noopener">')
    s = s.replace("{line}", '<a href="%s" target="_blank" rel="noopener">' % LINE)
    return s.replace("{/a}", "</a>")


def fr(s):
    return re.sub(r" ([:;?!])", " \\1", s)


arts, tabs = "", ""
for L, d in P.items():
    body = '<h1>%s</h1><p class="upd">%s</p><p class="lead">%s</p>' % (d["title"], d["upd"], d["lead"])
    for h, items in d["s"]:
        body += "<h2>%s</h2><ul>%s</ul>" % (h, "".join("<li>%s</li>" % link(x, d["hl"]) for x in items))
    if L == "fr":
        body = fr(body)
    arts += '<article id="pp-%s" lang="%s" data-title="%s" data-back="%s" hidden>\n%s\n</article>\n' % (L, L, d["title"], d["back"], body)
    tabs += '<button type="button" data-l="%s" lang="%s">%s</button>' % (L, L, d["name"])

s = src
s = s.replace("</nav>\n<article id=\"pp-en\"", tabs + "</nav>\n<article id=\"pp-en\"", 1)
s = s.replace("</article>\n</main>", "</article>\n" + arts + "</main>", 1)
a = "var ORDER=['en', 'ja', 'vi', 'id', 'zh', 'tw', 'ko'];"
assert a in s
s = s.replace(a, "var ORDER=['en', 'ja', 'vi', 'id', 'zh', 'tw', 'ko', 'de', 'fr', 'it', 'es', 'pt', 'tr'];")
s = s.replace("(location.search.match(/[?&]lang=([a-z]+)/)||[])[1]", "(location.search.match(/[?&]lang=([a-z]+)/)||[])[1]")
assert s.count("<article") == 13
os.makedirs(os.path.join(HERE, "out"), exist_ok=True)
open(os.path.join(HERE, "out", "privacypolicy.html"), "w", encoding="utf-8").write(s)
print("ok")
