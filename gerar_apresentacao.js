const {
  Document, Packer, Paragraph, TextRun, Table, TableRow, TableCell,
  AlignmentType, LevelFormat, BorderStyle, WidthType, ShadingType,
  HeadingLevel, VerticalAlign, Header, Footer, PageNumber
} = require("docx");
const fs = require("fs");

// === COLORS ===
const DARK_BLUE = "1F3864";
const LIGHT_GRAY = "F2F2F2";
const WHITE = "FFFFFF";
const MEDIUM_BLUE = "2E5FA3";
const ACCENT_BLUE = "D6E4F0";

// === DXA CONSTANTS (A4 with ~1.8cm margins) ===
const CONTENT_WIDTH = 9862;
const COL1 = 4680;
const COL2 = 5182;

// === HELPERS ===
function heading(text) {
  return new Paragraph({
    spacing: { before: 280, after: 100 },
    border: {
      bottom: { style: BorderStyle.SINGLE, size: 6, color: DARK_BLUE, space: 4 }
    },
    children: [new TextRun({
      text,
      bold: true,
      size: 26,
      font: "Arial",
      color: DARK_BLUE,
    })]
  });
}

function body(text, opts) {
  opts = opts || {};
  return new Paragraph({
    spacing: { before: 60, after: 60 },
    alignment: AlignmentType.JUSTIFIED,
    children: [new TextRun({
      text,
      font: "Arial",
      size: 20,
      bold: opts.bold || false,
      color: opts.color || "111111",
      italics: opts.italic || false,
    })]
  });
}

function bullet(text, bold) {
  return new Paragraph({
    numbering: { reference: "bullets", level: 0 },
    spacing: { before: 40, after: 40 },
    children: [new TextRun({
      text,
      font: "Arial",
      size: 20,
      bold: bold || false,
    })]
  });
}

function spacer(before) {
  return new Paragraph({
    spacing: { before: before || 80, after: 0 },
    children: [new TextRun({ text: "" })]
  });
}

// === BORDERS ===
const thinBorder = { style: BorderStyle.SINGLE, size: 4, color: "AAAAAA" };
const noBorder = { style: BorderStyle.NONE, size: 0, color: "FFFFFF" };
const leftAccentBorder = { style: BorderStyle.SINGLE, size: 20, color: DARK_BLUE };

function makeCell(lines, fill, isHeader, align) {
  align = align || AlignmentType.LEFT;
  return new TableCell({
    borders: { top: thinBorder, bottom: thinBorder, left: thinBorder, right: thinBorder },
    shading: { fill: fill, type: ShadingType.CLEAR },
    margins: { top: 100, bottom: 100, left: 160, right: 160 },
    verticalAlign: VerticalAlign.CENTER,
    children: lines.map(function(text) {
      return new Paragraph({
        alignment: align,
        spacing: { before: 20, after: 20 },
        children: [new TextRun({
          text: text,
          font: "Arial",
          size: 19,
          bold: isHeader || false,
          color: isHeader ? WHITE : "222222",
        })]
      });
    })
  });
}

// === DOCUMENT ===
const doc = new Document({
  numbering: {
    config: [
      {
        reference: "bullets",
        levels: [{
          level: 0,
          format: LevelFormat.BULLET,
          text: "\u2022",
          alignment: AlignmentType.LEFT,
          style: {
            paragraph: { indent: { left: 560, hanging: 280 } }
          }
        }]
      }
    ]
  },
  styles: {
    default: {
      document: { run: { font: "Arial", size: 20 } }
    }
  },
  sections: [{
    properties: {
      page: {
        size: { width: 11906, height: 16838 },
        margin: { top: 1022, right: 1022, bottom: 1022, left: 1022 }
      }
    },
    headers: {
      default: new Header({
        children: [
          new Paragraph({
            spacing: { before: 0, after: 120 },
            border: {
              bottom: { style: BorderStyle.SINGLE, size: 8, color: DARK_BLUE, space: 4 }
            },
            children: [
              new TextRun({
                text: "MIHMO  \u2022  Sistema Municipal de Per\u00edcias M\u00e9dicas",
                font: "Arial",
                size: 16,
                color: "888888",
              })
            ]
          })
        ]
      })
    },
    footers: {
      default: new Footer({
        children: [
          new Paragraph({
            spacing: { before: 120, after: 0 },
            border: {
              top: { style: BorderStyle.SINGLE, size: 4, color: "CCCCCC", space: 4 }
            },
            alignment: AlignmentType.RIGHT,
            children: [
              new TextRun({ text: "Abril de 2026  \u2022  P\u00e1gina ", font: "Arial", size: 16, color: "888888" }),
              new TextRun({ children: [PageNumber.CURRENT], font: "Arial", size: 16, color: "888888" }),
            ]
          })
        ]
      })
    },
    children: [

      // ─── TÍTULO ───────────────────────────────────────────────────
      new Paragraph({
        spacing: { before: 160, after: 40 },
        children: [new TextRun({
          text: "Proposta de Migra\u00e7\u00e3o",
          font: "Arial",
          size: 48,
          bold: true,
          color: DARK_BLUE,
        })]
      }),
      new Paragraph({
        spacing: { before: 0, after: 40 },
        children: [new TextRun({
          text: "Suporte T\u00e9cnico / QA  \u2192  Analista de QA",
          font: "Arial",
          size: 28,
          color: MEDIUM_BLUE,
        })]
      }),
      new Paragraph({
        spacing: { before: 40, after: 220 },
        border: {
          bottom: { style: BorderStyle.SINGLE, size: 14, color: DARK_BLUE, space: 6 }
        },
        children: [new TextRun({
          text: "Uma decis\u00e3o estrat\u00e9gica baseada em entregas reais",
          font: "Arial",
          size: 20,
          italics: true,
          color: "555555",
        })]
      }),

      // ─── 1. SITUAÇÃO ATUAL ────────────────────────────────────────
      heading("1. Situa\u00e7\u00e3o Atual"),
      body("Atualmente o trabalho est\u00e1 dividido entre duas fun\u00e7\u00f5es distintas e igualmente exigentes: suporte t\u00e9cnico de 1\u00ba e 2\u00ba n\u00edvel e quality assurance. Essa divis\u00e3o gera perda de profundidade em ambas as frentes \u2014 o suporte n\u00e3o recebe a aten\u00e7\u00e3o devida e os testes s\u00e3o constantemente interrompidos por urg\u00eancias operacionais."),

      spacer(100),

      new Table({
        width: { size: CONTENT_WIDTH, type: WidthType.DXA },
        columnWidths: [COL1, COL2],
        rows: [
          new TableRow({
            tableHeader: true,
            children: [
              makeCell(["Hoje (Suporte + QA)"], DARK_BLUE, true, AlignmentType.CENTER),
              makeCell(["Com foco exclusivo em QA"], MEDIUM_BLUE, true, AlignmentType.CENTER),
            ]
          }),
          new TableRow({ children: [
            makeCell(["Atendimento reativo a chamados"], LIGHT_GRAY, false),
            makeCell(["Cobertura de testes proativa e planejada"], WHITE, false),
          ]}),
          new TableRow({ children: [
            makeCell(["Testes interrompidos por urg\u00eancias"], LIGHT_GRAY, false),
            makeCell(["Ciclos de automa\u00e7\u00e3o cont\u00ednuos e est\u00e1veis"], WHITE, false),
          ]}),
          new TableRow({ children: [
            makeCell(["Contexto fragmentado entre duas \u00e1reas"], LIGHT_GRAY, false),
            makeCell(["Especializa\u00e7\u00e3o profunda no dom\u00ednio do sistema"], WHITE, false),
          ]}),
          new TableRow({ children: [
            makeCell(["Bugs identificados apenas em produ\u00e7\u00e3o"], LIGHT_GRAY, false),
            makeCell(["Bugs capturados antes de chegar ao cliente"], WHITE, false),
          ]}),
        ]
      }),

      spacer(180),

      // ─── 2. O QUE JÁ FOI ENTREGUE ────────────────────────────────
      heading("2. O Que J\u00e1 Foi Entregue em QA"),
      body("Por iniciativa pr\u00f3pria, foi constru\u00eddo um framework de automa\u00e7\u00e3o completo para o sistema Mihmo, sem solicita\u00e7\u00e3o formal e sem prazo definido. As entregas abaixo s\u00e3o concretas e verificadas:"),
      spacer(80),

      new Table({
        width: { size: CONTENT_WIDTH, type: WidthType.DXA },
        columnWidths: [CONTENT_WIDTH],
        rows: [
          new TableRow({
            children: [new TableCell({
              borders: {
                top: noBorder,
                bottom: noBorder,
                left: leftAccentBorder,
                right: noBorder
              },
              shading: { fill: LIGHT_GRAY, type: ShadingType.CLEAR },
              margins: { top: 140, bottom: 140, left: 280, right: 180 },
              children: [
                new Paragraph({
                  spacing: { before: 0, after: 80 },
                  children: [new TextRun({
                    text: "Framework de Automa\u00e7\u00e3o \u2014 Evid\u00eancias",
                    font: "Arial", size: 20, bold: true, color: DARK_BLUE
                  })]
                }),
                bullet("Tecnologias: Robot Framework + Python + Playwright / Browser Library"),
                bullet("Cria\u00e7\u00e3o autom\u00e1tica de massa de servidores e funcion\u00e1rios via API (zero interven\u00e7\u00e3o manual)"),
                bullet("Cobertura de regras de neg\u00f3cio para m\u00faltiplas prefeituras: PMV (Vit\u00f3ria) e PPV (Porto Velho)"),
                bullet("Cen\u00e1rios de borda com dias limites e c\u00f3digos CID \u2014 casos raramente cobertos em testes manuais"),
                bullet("Gera\u00e7\u00e3o de massa_criada.json com rastreabilidade total: nome, CPF, customer_id e CID utilizados"),
                bullet("D\u00fazias de cen\u00e1rios executados em minutos, com log completo de cada execu\u00e7\u00e3o"),
              ]
            })]
          })
        ]
      }),

      spacer(180),

      // ─── 3. POR QUE FAZ SENTIDO PARA A EMPRESA ───────────────────
      heading("3. Por Que Faz Sentido para a Empresa"),
      body("A migra\u00e7\u00e3o n\u00e3o \u00e9 um benef\u00edcio pessoal \u2014 \u00e9 uma decis\u00e3o de produto. Os riscos de manter o modelo atual s\u00e3o diretos:"),
      spacer(60),
      bullet("Bugs em regras de per\u00edcia afetam prefeituras clientes e geram retrabalho caro de corre\u00e7\u00e3o"),
      bullet("Sem foco dedicado, o framework existente n\u00e3o evolui e o investimento j\u00e1 feito n\u00e3o \u00e9 aproveitado"),
      bullet("Cada hora de suporte \u00e9 uma hora a menos de cobertura sobre fluxos cr\u00edticos do sistema"),
      bullet("PMV e PPV possuem regras distintas; a complexidade do dom\u00ednio exige especializa\u00e7\u00e3o sustentada"),

      spacer(180),

      // ─── 4. O QUE SERÁ ENTREGUE ──────────────────────────────────
      heading("4. O Que Ser\u00e1 Entregue com Foco Exclusivo em QA"),
      body("Com dedica\u00e7\u00e3o integral \u00e0 fun\u00e7\u00e3o, os compromissos s\u00e3o:"),
      spacer(60),
      bullet("Expans\u00e3o da cobertura para todos os fluxos cr\u00edticos de per\u00edcia do Mihmo", true),
      bullet("Integra\u00e7\u00e3o dos testes ao pipeline de CI/CD \u2014 qualidade verificada a cada deploy", true),
      bullet("Documenta\u00e7\u00e3o viva das regras de neg\u00f3cio via cen\u00e1rios de teste leg\u00edveis", true),
      bullet("Suporte estruturado a novas prefeituras: onboarding de regras com testes desde o primeiro dia", true),
      bullet("Redu\u00e7\u00e3o mensur\u00e1vel de bugs em produ\u00e7\u00e3o nos primeiros 90 dias", true),

      spacer(180),

      // ─── 5. PRÓXIMO PASSO ─────────────────────────────────────────
      heading("5. Pr\u00f3ximo Passo"),

      new Table({
        width: { size: CONTENT_WIDTH, type: WidthType.DXA },
        columnWidths: [CONTENT_WIDTH],
        rows: [
          new TableRow({
            children: [new TableCell({
              borders: { top: thinBorder, bottom: thinBorder, left: thinBorder, right: thinBorder },
              shading: { fill: ACCENT_BLUE, type: ShadingType.CLEAR },
              margins: { top: 160, bottom: 160, left: 240, right: 240 },
              children: [
                new Paragraph({
                  alignment: AlignmentType.CENTER,
                  spacing: { before: 0, after: 80 },
                  children: [new TextRun({
                    text: "Solicito uma reuni\u00e3o de 30 minutos para alinhar a transi\u00e7\u00e3o.",
                    font: "Arial", size: 22, bold: true, color: DARK_BLUE,
                  })]
                }),
                new Paragraph({
                  alignment: AlignmentType.CENTER,
                  spacing: { before: 0, after: 0 },
                  children: [new TextRun({
                    text: "O framework j\u00e1 existe, os resultados j\u00e1 existem \u2014 o que falta \u00e9 o contexto para acelerar.",
                    font: "Arial", size: 20, italics: true, color: "444444",
                  })]
                }),
              ]
            })]
          })
        ]
      }),

    ]
  }]
});

Packer.toBuffer(doc).then(function(buffer) {
  fs.writeFileSync("C:/dev/qa/apresentacao_migracao_qa.docx", buffer);
  console.log("Arquivo gerado: C:/dev/qa/apresentacao_migracao_qa.docx");
  console.log("Tamanho: " + (buffer.length / 1024).toFixed(1) + " KB");
});
