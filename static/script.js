async function iniciarDownload() {

    const url =
        document.querySelector("#url").value.trim();

    const formato =
        document.querySelector("#formato").value;

    const qualidade =
        document.querySelector("#qualidade").value;

    const botao =
        document.querySelector("#botao-download");

    const status =
        document.querySelector("#status");

    const sucesso =
        document.querySelector("#sucesso");

    const arquivo =
        document.querySelector("#arquivo");


    if (!url) {

        status.textContent =
            "⚠ Cole uma URL do YouTube.";

        return;
    }


    botao.disabled = true;

    botao.textContent =
        "⏳ BAIXANDO...";


    status.textContent =
        "● Preparando download...";


    sucesso.style.display =
        "none";


    try {

        const resposta =
            await fetch(
                "/download",
                {

                    method: "POST",

                    headers: {
                        "Content-Type":
                            "application/json"
                    },

                    body: JSON.stringify({

                        url: url,

                        formato: formato,

                        qualidade: qualidade

                    })
                }
            );


        const dados =
            await resposta.json();


        if (dados.sucesso) {


            status.textContent =
                "✓ Download concluído!";


            sucesso.style.display =
                "block";


            arquivo.innerHTML = `

                <strong>
                    ${dados.arquivo}
                </strong>

                <a
                    href="${dados.url_download}"
                    class="botao-arquivo"
                    download
                >
                    ⬇ BAIXAR ARQUIVO
                </a>

            `;


        } else {


            status.textContent =
                "✕ " + dados.erro;

        }


    } catch (erro) {


        console.error(erro);


        status.textContent =
            "✕ Erro de comunicação com o servidor.";

    }


    finally {

        botao.disabled = false;

        botao.textContent =
            "⬇ BAIXAR";

    }

}