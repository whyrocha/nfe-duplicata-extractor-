import xml.etree.ElementTree as ET
import csv
from pathlib import Path

def extrair_duplicatas(xml_path: str):
    xml_path = Path(xml_path)
    tree = ET.parse(xml_path)
    root = tree.getroot()

    # Descobrir o namespace automaticamente (ex.: "http://www.portalfiscal.inf.br/nfe")
    if root.tag.startswith("{"):
        ns_uri = root.tag[1:].split("}")[0]
    else:
        ns_uri = "http://www.portalfiscal.inf.br/nfe"

    ns = {"nfe": ns_uri}
    dados = []

    # Em muitos XMLs de NFe o NFe está dentro de <nfeProc>
    nfe = root.find("nfe:NFe", ns)
    if nfe is None:
        # fallback: caso o root já seja <NFe>
        if root.tag.endswith("NFe"):
            nfe = root
        else:
            print(f"[AVISO] Nó <NFe> não encontrado em {xml_path.name}")
            return dados  # volta vazio

    infNFe = nfe.find("nfe:infNFe", ns)
    if infNFe is None:
        print(f"[AVISO] <infNFe> não encontrado em {xml_path.name}")
        return dados

    # Número da NF
    nNF_el = infNFe.find("nfe:ide/nfe:nNF", ns)
    numero_nf = nNF_el.text if nNF_el is not None else ""

    # Cobrança / duplicatas
    cobr = infNFe.find("nfe:cobr", ns)
    if cobr is None:
        print(f"[INFO] XML {xml_path.name} não possui <cobr> (sem duplicatas).")
        return dados

    for dup in cobr.findall("nfe:dup", ns):
        nDup_el = dup.find("nfe:nDup", ns)
        dVenc_el = dup.find("nfe:dVenc", ns)
        vDup_el = dup.find("nfe:vDup", ns)

        dados.append({
            # "arquivo_xml": xml_path.name,  # removido do CSV
            "numero_nf": numero_nf,
            "numero_parcela": nDup_el.text if nDup_el is not None else "",
            "data_vencimento": dVenc_el.text if dVenc_el is not None else "",
            "valor_duplicata": vDup_el.text if vDup_el is not None else "",
        })

    print(f"[OK] {xml_path.name} → {len(dados)} duplicata(s) encontrada(s).")
    return dados


def gerar_csv_pasta(pasta_xml: str, csv_path: str):
    pasta = Path(pasta_xml)

    # DEBUG: listar arquivos encontrados
    xml_files = list(pasta.glob("*.xml"))
    print(f"Procurando XMLs em: {pasta.resolve()}")
    print(f"Arquivos .xml encontrados: {len(xml_files)}")
    for f in xml_files:
        print(" -", f.name)

    todos_registros = []

    for xml_file in xml_files:
        try:
            registros = extrair_duplicatas(xml_file)
            if registros:
                todos_registros.extend(registros)
        except Exception as e:
            print(f"[ERRO] ao processar {xml_file.name}: {e}")

    if not todos_registros:
        print("Nenhuma duplicata encontrada em nenhum XML. CSV não será criado.")
        return
    
    # Agora sem 'arquivo_xml'
    campos = ["numero_nf", "numero_parcela", "data_vencimento", "valor_duplicata"]

    with open(csv_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=campos, delimiter=";")
        writer.writeheader()
        writer.writerows(todos_registros)

    print(f"CSV gerado em: {csv_path}")


if __name__ == "__main__":
    # caminho da pasta onde estão os XMLs
    pasta_xml = r"C:\Users\ContsCar\Desktop\Nova pasta\duplicata_csv\xmls"
    # nome/onde será criado o CSV (na mesma pasta do .py, se você rodar de lá)
    csv_saida = r"duplicatas_nfs.csv"

    gerar_csv_pasta(pasta_xml, csv_saida)