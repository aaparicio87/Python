'use strict';

$(function() {
    $("#cubacel").click(function () {	 
                $("#tab_cellphone").tab('show')
                $("input[name='cellphone']").val('');
                $("input[name='nauta']").val('');
                $.get( "/get_cell_offers", function( data ) {
                    $("#offerts").html("");
                    create_card(data);
                  }); 
                $("#tab_nauta").removeClass('active').addClass('hide');
                $("#tab_submit").removeClass('active').addClass('hide');
                $(".option-error").removeClass("alert alert-danger")
                $(".option-error").html("")
                
    });           
    $("#nauta").click(function () {	 
                $("#tab_nauta").tab('show');
                $("input[name='nauta']").val('');
                $("input[name='cellphone']").val('');
                $.get( "/get_nauta_offers", function( data ) {
                    $("#offerts").html("");
                    create_card(data);
                }); 
                $("#tab_cellphone").removeClass('active').addClass('hide');
                $("#tab_submit").removeClass('active').addClass('hide');
                $(".option-error").removeClass("alert alert-danger");
                $(".option-error").html("");
    });
       

     $("input[type='text']").keyup(function(e) {
        const regex = /^\(?([0-9]{8})$/;
        let cell = $(this).val();
        $(".option-error").removeClass("alert alert-danger");
        $(".option-error").html("");
        $('input[name="select-amount"]').prop('checked', false);
        if(cell.match(regex)){
            
            e.preventDefault();
            return false;
        }
        
    });

    $("input[type='email']").keyup(function(e) {
        const regex = /(\W|^)[\w.+\-]*@nauta.com\.cu(\W|$)/;
        let nauta = $(this).val();
        $(".option-error").removeClass("alert alert-danger");
        $(".option-error").html("");
        $('input[name="select-amount"]').prop('checked', false);
        if(nauta.match(regex)){
            
            e.preventDefault();
            return false;
        }
        
    });

    $(".btn-modal").click(function(){
        const id = $('input[name="select-amount"]:checked').val();
        const label_id =`label${id}`;
        const elms = document.getElementById(label_id).getElementsByTagName("*");
        loadModalForm($("input[name='cellphone']").val(), $("input[name='nauta']").val(), elms[0].innerHTML, elms[1].innerHTML,id);
    });   
});

const create_card = (data) =>{
    let object_data = JSON.parse(data);
    
   
    object_data.forEach(element => {
        add_data(element.pk, element.fields.name, element.fields.price) ;
    });
    
}

const add_data = (pk, name, price) =>{
    let eur = price/24;
    let cup = price
    const div1 = '<div class="col-lg-3 col-sm-5 col-md-5 px-lg-3"  id="first_div'+pk+'"></div>';
    const label = '<label class="form-group-small eto-card border-dark btn btn-sm" id="label'+pk+'"></label>';
    const div2 = `<div id="monto">${eur.toFixed(2)} €</div>`+`<div id="recibe">${cup} CUP</div>`
    +'<input type="radio" name="select-amount"  value="'+pk+'" onchange="getValue()">';
        $(" #offerts ").append(div1);
        $(`#first_div${pk}`).append(label);
        $(`#label${pk}`).append(div2);
}

const getValue = () =>{
    const regex_cell = /^\(?([0-9]{8})$/;
    const regex_nauta = /(\W|^)[\w.+\-]*@nauta.com\.cu(\W|$)/;
    if($("input[name='cellphone']").val().match(regex_cell) ){
      $("#tab_submit").tab('show');
    }
    else if($("input[name='nauta']").val().match(regex_nauta)){ 
    $("#tab_submit").tab('show');
    }
    else{
        $(".option-error").addClass("alert alert-danger");
        $(".option-error").html("Rellene este campo con los valores correctos ");
    }
}

const loadModalForm = (cellphone, nauta, euro, cup, id) =>{

    const lb_benef = $("#lb_benef");
    const tb_benef= $('input[name="benef"]');
    const tb_cant_cup = $('input[name="cant_cup"]');
    const tb_cant_euro = $('input[name="cant_euro"]');
    const tb_hidden = $('input[name="oculto"]');
    const tb_hidden1 = $('input[name="oculto1"]');

    if(cellphone === ""){
        lb_benef.html("");
        tb_benef.html("");
        lb_benef.html("Cuenta del beneficiado");
        tb_benef.val(nauta);
        tb_cant_euro.val(euro);
        tb_cant_cup.val(cup);
        tb_hidden.val("nauta");
        tb_hidden1.val(id);
    }
    else{
    lb_benef.html("");
    tb_benef.html("");
    lb_benef.html("Numero del beneficiado");
    tb_benef.val(`+53${cellphone}`);
    tb_cant_euro.val(euro);
    tb_cant_cup.val(cup);
    tb_hidden.val("cubacel");
    tb_hidden1.val(id);
    }

}