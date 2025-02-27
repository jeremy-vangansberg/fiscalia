erDiagram
    BOFIP_DOCUMENTS {
      INT id PK "Identifiant unique"
      VARCHAR document_identifier "Identifiant du document (ex: BOI-LETTRE-000048-20130826)"
      VARCHAR title "Titre extrait de dc:title"
      DATE publication_date "Date extraite de dc:date"
      VARCHAR creator "Créateur extrait de dc:creator"
      VARCHAR document_type "Type de document (ex: Lettre Type, Commentaire, etc.)"
      VARCHAR file_path "Chemin complet dans l'arborescence"
      VARCHAR data_html_file "Nom du fichier HTML (data.html)"
      VARCHAR document_xml_file "Nom du fichier XML (document.xml)"
      LONGTEXT html_content "Contenu HTML extrait de data.html"
      JSON metadata "Métadonnées complètes du document XML transformées en JSON"
      TIMESTAMP date_import "Date d'importation"
    }
