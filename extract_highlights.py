#!/usr/bin/env python3

import fitz  # PyMuPDF
import os
import argparse

# Referenzfarben (RGB) mit Namen für Farbabgleich
REFERENCE_COLORS = {
    "Gelb":   (1.0, 1.0, 0.0),
    "Rot":    (1.0, 0.0, 0.0),
    "Grün":   (0.0, 1.0, 0.0),
    "Blau":   (0.0, 0.0, 1.0),
    "Türkis": (0.0, 1.0, 1.0),
    "Magenta":(1.0, 0.0, 1.0),
    "Orange": (1.0, 0.5, 0.0),
    "Grau":   (0.5, 0.5, 0.5),
}

# Reihenfolge der Farben für Ausgabe
COLOR_ORDER = ["Gelb", "Rot", "Grün", "Blau", "Türkis", "Magenta", "Orange", "Grau", "Unbekannt"]

def color_distance(c1, c2):
    """Berechnet die euklidische Distanz zwischen zwei RGB-Farben."""
    return sum((a - b) ** 2 for a, b in zip(c1, c2)) ** 0.5

def match_color_name(rgb, tolerance=0.15):
    """
    Findet den Farbnamen mit der geringsten Distanz zu rgb innerhalb der Toleranz.
    Rückgabe: Farbnamen oder "Unbekannt".
    """
    best_match = "Unbekannt"
    min_dist = float('inf')
    for name, ref_rgb in REFERENCE_COLORS.items():
        dist = color_distance(rgb, ref_rgb)
        if dist < min_dist and dist <= tolerance:
            min_dist = dist
            best_match = name
    return best_match

def extract_highlights_by_color(pdf_path):
    """
    Extrahiert alle Highlight-Anmerkungen aus der PDF,
    liest den markierten Text basierend auf Quadpoints,
    und ordnet sie farblich zu.
    Rückgabe: Liste von Tupeln (Farbe, Seitenzahl, Text).
    """
    doc = fitz.open(pdf_path)
    highlights = []

    for page_number, page in enumerate(doc, start=1):
        for annot in page.annots():
            # Nur Highlight-Anmerkungen (Typ 8)
            if annot.type[0] != 8:
                continue

            quadpoints = annot.vertices
            if not quadpoints:
                continue

            words = page.get_text("words")  # alle Wörter mit Bounding-Box und Text
            text_fragments = []

            # Quadpoints sind in 4er-Gruppen (jeweils ein Rechteck)
            for i in range(0, len(quadpoints), 4):
                rect = fitz.Quad(quadpoints[i:i+4]).rect
                for w in words:
                    word_rect = fitz.Rect(w[:4])

                    # Schnittfläche zwischen Markierung und Wortbox
                    intersection = rect & word_rect

                    # Nur Wörter mit mindestens 50% Überlappung aufnehmen
                    if intersection.get_area() / word_rect.get_area() > 0.5:
                        text_fragments.append(w[4])

            if not text_fragments:
                continue

            # Zusammensetzen der extrahierten Wörter zu einem Text
            text = " ".join(text_fragments).strip()

            # Farbwert der Annotation (Stroke color) abrufen (RGB Werte zwischen 0 und 1)
            color_rgb = annot.colors.get("stroke", (0, 0, 0))
            color_rgb = tuple(round(x, 2) for x in color_rgb)
            color_name = match_color_name(color_rgb)

            highlights.append((color_name, page_number, text))

    return highlights

def save_to_markdown(highlights, output_path):
    """
    Speichert die gesammelten Highlights gruppiert nach Farbe und Seite in eine Markdown-Datei.
    """
    # Sortieren nach Farbe mit Default-Liste
    sorted_by_color = {color: [] for color in COLOR_ORDER}
    for color, page, text in highlights:
        sorted_by_color.setdefault(color, []).append((page, text))

    with open(output_path, 'w', encoding='utf-8') as f:
        f.write("# Hervorhebungen nach Farbe\n\n")
        for color in COLOR_ORDER:
            items = sorted_by_color.get(color, [])
            if not items:
                continue
            f.write(f"## {color}\n\n")
            for page, text in items:
                f.write(f"### Seite {page}\n{text}\n\n")

def main():
    parser = argparse.ArgumentParser(description="Extrahiere farbige Highlights aus einer PDF-Datei und speichere sie als Markdown.")
    parser.add_argument("pdf_path", help="Pfad zur PDF-Datei")
    parser.add_argument("output_md", help="Zielpfad für die Markdown-Datei")
    args = parser.parse_args()

    if not os.path.exists(args.pdf_path):
        print("Fehler: Die angegebene PDF-Datei wurde nicht gefunden.")
        return

    highlights = extract_highlights_by_color(args.pdf_path)
    save_to_markdown(highlights, args.output_md)
    print(f"{len(highlights)} Highlights extrahiert und gespeichert in '{args.output_md}'.")

if __name__ == "__main__":
    main()