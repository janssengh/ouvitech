// função para preencher os campos do formulario
const preencher_formulario = (produto) => {

    document.getElementById('descricao').value = produto.name;
    document.getElementById('paginas').value = produto.pages;


}

// Atualiza dados do formulário via método PUT
const atualizar = () =>{

    if (!validar_formulario())
        return;
}