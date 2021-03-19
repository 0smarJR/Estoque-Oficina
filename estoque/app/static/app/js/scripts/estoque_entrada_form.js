$(document).ready(function() {
    c = 0
    var data = new Date();
    var dia = data.getDate();
    var mes = data.getMonth();
    var ano = data.getFullYear();
    var hora = data.getHours();
    var min = data.getMinutes();
    var seg = data.getSeconds();
    var nota = dia.toString() + (mes + 1).toString() + ano.toString() + hora.toString() + min.toString() + seg.toString()
    $("#id_main-nf").val(nota)
    $(".help-block").text('*')
    $("#user").hide()
    usuario = $("#user").text()
    $("select option").filter(function() {
        //may want to use $.trim in here
        return $(this).text() == usuario;
    }).prop('selected', true);
    $("#id_main-usuario").prop("disabled", true);
    $("#id_main-nf").prop("disabled", true);
    $("#id_estoque-0-saldo").prop("disabled", true);
    $('#id_estoque-0-saldo').after('<input id="id_estoque-0-inicial" class="form-control" type="hidden"></input>');

    // Insere classe no primeiro item de produto
    $('#id_estoque-0-produto').addClass('clProduto');
    $('#id_estoque-0-quantidade').addClass('clQuantidade');
    $('.clProduto').select2()
    $('.control-label').each(function (index) {
        $(this).css("margin", "10px")
    })

    $('#add-item').click(function(ev) {
        ev.preventDefault();
        count = $('#estoque').children().length;
        var tmplMarkup = $('#item-estoque').html();
        var compiledTmpl = tmplMarkup.replace(/__prefix__/g, count);
        $('div#estoque').append(compiledTmpl);

        // update form count
        $('#id_estoque-TOTAL_FORMS').attr('value', count + 1);

        // some animate to scroll to view our new form
        //$('html, body').animate({
        //  scrollTop: $("#add-item").position().top - 200
        //}, 800);

        $('#id_estoque-' + (count) + '-produto').addClass('clProduto');
        $('#id_estoque-' + (count) + '-quantidade').addClass('clQuantidade');
        $("#id_estoque-" + count + "-saldo").prop("disabled", true);
        $('#id_estoque-'+ count +'-saldo').after('<input id="id_estoque-' + count + '-inicial" class="form-control" type="hidden"></input>');
        $('.clProduto').select2()
        $('.control-label').each(function (index) {
            $(this).css("margin", "10px")
        })
    });

    let estoque
    let saldo
    let campo
    let quantidade

    $(document).on('change', '.clProduto', function() {
        let self = $(this)
        let pk = $(this).val()
        let url = '/products/' + pk + '/json/'

        $.ajax({
            url: url,
            type: 'GET',
            success: function(response) {
                estoque = response.data[0].estoque
                campo = self.attr('id').replace('produto', 'quantidade')
                estoque_inicial = self.attr('id').replace('produto', 'inicial')
                $('#'+estoque_inicial).val(estoque)
                    // Remove o valor do campo 'quantidade'
                $('#' + campo).val('')
            },
            error: function(xhr) {
                // body...
            }
        })
    });

    $(document).on('change', '.clQuantidade', function() {
        quantidade = $(this).val();
        campo = $(this).attr('id').replace('quantidade', 'saldo')
        campo_estoque_inicial = $(this).attr('id').replace('quantidade', 'inicial')
        estoque_inicial = $('#'+campo_estoque_inicial).val()
        saldo = Number(quantidade) + Number(estoque_inicial);
        // Atribui o saldo ao campo 'saldo'
        $('#' + campo).val(saldo)
    });

    $('#salvar').click(function() {
        $("#id_main-usuario").prop("disabled", false);
        $("#id_estoque-0-saldo").prop("disabled", false);
        $("#id_main-nf").prop("disabled", false);
        c = 0
        while (c <= count) {
            $("#id_estoque-" + c + "-saldo").prop("disabled", false);
            c = c + 1
        }
    });
});