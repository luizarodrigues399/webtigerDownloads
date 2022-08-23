function login(){
   //document.getElementById('myModal').style.display = 'block';
   $.ajax({
    type: "POST",
    url: "login",
    data: JSON.stringify({
      'username':document.getElementById('username').value,
      'password':document.getElementById('password').value,
    }),
    contentType: 'application/json;charset=UTF-8',
    success: function (data) {
      if (data!='ok')
        alert(data);
      else{
         $.ajax({
          type: "POST",
          url: "interfaceInicial",
          contentType: 'application/json;charset=UTF-8',
          success: function (data) {
            if (data=='Sessão expirada!'){
              alert(data);
              window.location='/';
            }
            window.location='interfaceInicial';
          } });
    }
   } });
}

function myOnLoadedData(audio) {
  document.getElementById('carregandoAudio'+audio).innerHTML = ' ';
}

function pressWord (checkbox) {
  if (checkbox.checked){
     document.forms['nextPage'].elements["WORDhidden"].value= 'checked';
      document.forms['previousPage'].elements["WORDhidden"].value= 'checked';
       document.forms['firstPage'].elements["WORDhidden"].value= 'checked';
        document.forms['lastPage'].elements["WORDhidden"].value= 'checked';
        console.log('WORDchecked');
  }
  else{
     document.forms['nextPage'].elements["WORDhidden"].value= '';
      document.forms['previousPage'].elements["WORDhidden"].value= '';
       document.forms['firstPage'].elements["WORDhidden"].value= '';
        document.forms['lastPage'].elements["WORDhidden"].value= '';
         console.log('WORDnaoChecked');
  }
}

function pressPDF (checkbox) {
  if (checkbox.checked){
     document.forms['nextPage'].elements["PDFhidden"].value= 'checked';
      document.forms['previousPage'].elements["PDFhidden"].value= 'checked';
       document.forms['firstPage'].elements["PDFhidden"].value= 'checked';
        document.forms['lastPage'].elements["PDFhidden"].value= 'checked';
        console.log('PDFchecked');
  }
  else{
     document.forms['nextPage'].elements["PDFhidden"].value= '';
      document.forms['previousPage'].elements["PDFhidden"].value= '';
       document.forms['firstPage'].elements["PDFhidden"].value= '';
        document.forms['lastPage'].elements["PDFhidden"].value= '';
         console.log('PDFnaoChecked');
  }
}

//======================== COOKIE ===========================================
function getCookie( name ) {
  console.log(document.cookie.split(';'));
  var parts = document.cookie.split(name + "=");
  if (parts.length == 2) return parts.pop().split(";").shift();
}

function expireCookie( cName ) {
    document.cookie = 
        encodeURIComponent(cName + "=deleted; expires=" + new Date( 0 ).toUTCString());
}

function createToken() {
    var downloadToken = new Date().getTime();
    console.log('downloadToken:'+downloadToken);
    document.getElementById("downloadToken").value = downloadToken;
    return downloadToken;
}

var downloadTimer;
var attempts = 100;

function blockResubmit() {
    var downloadToken = createToken();
    downloadTimer = window.setInterval( function() {
        var token = getCookie( "downloadToken" ); //Cookie setado no Flask main.py, quando volta a resposta do donwload

        if(token == downloadToken) //|| (attempts == 0) ) 
            unblockSubmit();

        //attempts--;
    }, 1000 );
}

function unblockSubmit() {
  document.getElementById('myModal').style.display = 'none';
  console.log('Completo');
  window.clearInterval( downloadTimer );
  expireCookie( "downloadToken" );
}
//======================================================================

var loading=1;

function carregando (){
  document.getElementById('myModal').style.display = 'block';

  $.ajax({
    type: "POST",
    url: "search",
    data: JSON.stringify({
      'IDCall':document.getElementById('IDCall').value,
      'initialDate':document.getElementById('initialDate').value,
      'initialHourHidden':document.getElementById('initialHourHidden').value,
      'endDate':document.getElementById('endDate').value,
      'endHourHidden':document.getElementById('endHourHidden').value,
      'DDDtelephoneTarget':document.getElementById('DDDtelephoneTarget').value,
      'telephoneTarget':document.getElementById('telephoneTarget').value,
      'DDDtelephoneInter':document.getElementById('DDDtelephoneInter').value,
      'telephoneInter':document.getElementById('telephoneInter').value,
      'operation':document.getElementById('operation').value,
      'target':document.getElementById('target').value,
      'agent':document.getElementById('agent').value,
      'transcription':document.getElementById('transcription').value,
      'transcriptionPartHidden':document.getElementById('transcriptionPartHidden').value,
      'sinopse':document.getElementById('sinopse').value,
      'sinopsePartHidden':document.getElementById('sinopsePartHidden').value,
      'priority':document.getElementById('priority').value,
      'directionCall':document.getElementById('directionCall').value,
      'listening':document.getElementById('listening').value,
      'process':document.getElementById('process').value,
      'callswithAudio':document.getElementById('callswithAudio').value,
      'callswithPhoto':document.getElementById('callswithPhoto').value,
      'browser':document.getElementById('browser').value,
    }),
    contentType: 'application/json;charset=UTF-8',
   success: function (data) {
      if (data == 'Erro de conexão com o Banco de Dados') {
        alert(data);
        document.getElementById('myModal').style.display ='none';
        window.location = "interfaceInicial"; 
      }
      if (data == 'Sessão Expirada') {
        alert(data);
        document.getElementById('myModal').style.display ='none';
        window.location = "interfaceInicial"; 
      }
      else{
          document.getElementById('caption').innerHTML='Retornando registros, aguarde...';   
          var i=0;
          if (typeof(data)=='string') {
             document.getElementById('myModal').style.display ='none';
             var myWindow = window.open("", "_self");
             myWindow.document.write(data);
           }
          else { 
              while ( (i< data['rowsToDownload'].length) && (document.getElementById('myModal').style.display !='none') ) {
                     var ajax= $.ajax({
                        type: "POST",
                        url: "transferDataServer",
                        data: JSON.stringify({  'file': data['rowsToDownload'][i],
                                                'NameDir': data['NameDir'],
                                                'comFoto': data['comFoto'],
                                                'i': i }),
                        contentType: 'application/json;charset=UTF-8',
                        success: function (file) {
                            porcentagem=(Math.round( (loading*100)/data['lenght'] ) );
                            document.getElementById('loading').style.width= porcentagem.toString()+'%';
                            loading=loading+1;

                          if (file== 'Erro de conexão com o FTP') {
                            if (document.getElementById('myModal').style.display !='none')
                              alert(file);
                            document.getElementById('myModal').style.display ='none';
                            window.location = "interfaceInicial";
                          }
                          else{
                            if ($.active<=5)
                              document.getElementById('loading').style.width=='100%';
                            if ($.active<=1){
                               var date = new Date();
                               var curDate = null;
                               do { curDate = new Date();
                                    console.log('TEMPO'); }
                               while(curDate-date < 3000);

                              $.ajax({
                                type: "POST",
                                url: "renderPage",
                                data: JSON.stringify({  'rows': data['rows'],
                                                        'NameDir': data['NameDir'],
                                                        'comFoto': data['comFoto'],
                                                        'browser' : data['browser'], 
                                                        'lenght': data['lenght'],
                                                        'rawQuery': data['rawQuery'],
                                                        'nomOper': data['nomOper'],
                                                      }),
                                contentType: 'application/json;charset=UTF-8',
                                success: function (data) {
                                  var myWindow = window.open("", "_self");
                                  myWindow.document.write(data);
                                } 
                              });
                            } 
                          }
                        }
                      });
                i++;
              } 
            }
      }
    }
   });
}

function submitButton(){
  if (document.getElementById("quaisCheckboxes").value) 
    return true;
  
  else {
    alert('Nenhum registro foi selecionado');  
    return false;
  }
}

function carregandoDownloadCliente (){
  document.getElementById('myModal').style.display = 'block';
  document.getElementById('caption').innerHTML='Criando HTML, aguarde...';
  document.getElementById('loading').style.width='20%';
}

function Download(){
  window.stop();
  var ok= submitButton(); 

  if (ok==true) {
    blockResubmit(); 
    carregandoDownloadCliente();

      $.ajax({
      type: "POST",
      url: "downloadHTML",
      data: JSON.stringify({
        'NameDir':document.getElementById('NameDir').value,
        'downloadToken':document.getElementById('downloadToken').value,
        'quaisCheckboxes':document.getElementById('quaisCheckboxes').value,
        'callswithPhoto':document.getElementById('comFotos').value
      }),
      contentType: 'application/json;charset=UTF-8',
      success: function (data) {
        if (data == 'Sessão Expirada'){
          alert(data);
          document.getElementById('myModal').style.display ='none';
          window.location = "/"; 
        }
        else {
          if ( (data == 'Erro para baixar arquivos estáticos') || (data == 'Erro de conexão com o Banco de Dados') || (data == 'Erro ao baixar o HTML')  ) {
            alert(data);
            document.getElementById('myModal').style.display ='none';
            window.location = "interfaceInicial"; 
          } 
          else{
              if (document.getElementById('WORD').checked==true){
                document.getElementById('loading').style.width= '40%';
                document.getElementById('caption').innerHTML='Criando WORD, aguarde...';
              }
            $.ajax({
            type: "POST",
            url: "downloadWord",
            data: JSON.stringify({
              'NameDir': document.getElementById('NameDir').value,
              'callswithPhoto': document.getElementById('comFotos').value,
              'WORDdownload': document.getElementById('WORD').checked,
              'fileRows': data
            }),
            contentType: 'application/json;charset=UTF-8',
            success: function (resultadoWord) {
                console.log(resultadoWord);
                if (resultadoWord != 'ok') {
                  alert(resultadoWord);
                  document.getElementById('myModal').style.display ='none';
                  window.location = "interfaceInicial"; 
                } 

                if (document.getElementById('PDF').checked==true){
                  document.getElementById('loading').style.width='60%';
                  document.getElementById('caption').innerHTML='Criando PDF, aguarde...';
                  }
                $.ajax({
                type: "POST",
                url: "downloadPDF",
                data: JSON.stringify({
                  'NameDir':document.getElementById('NameDir').value,
                  'callswithPhoto':document.getElementById('comFotos').value,
                  'PDFdownload': document.getElementById('PDF').checked,
                  'fileRows': data
                }),
                contentType: 'application/json;charset=UTF-8',
                success: function (resultadoPDF) {
                    console.log(resultadoPDF);
                    if (resultadoPDF != 'ok') {
                      alert(resultadoPDF);
                      document.getElementById('myModal').style.display ='none';
                      window.location = "interfaceInicial"; 
                    }
                    document.getElementById('loading').style.width='80%';
                    document.getElementById('caption').innerHTML='Copiando arquivos para zipar, aguarde...';
                    var i=0;
                    while ( (i< data.length) && (document.getElementById('myModal').style.display !='none') ) {
                     $.ajax({
                      type: "POST",
                      url: "copyImageAudio",
                      data: JSON.stringify({
                        'file':data[i],
                        'NameDir':document.getElementById('NameDir').value,
                      }),
                      contentType: 'application/json;charset=UTF-8',
                      success: function (data) {
                        if ($.active<=1) {
                         document.getElementById('loading').style.width=='100%';
                         var date = new Date();
                         var curDate = null;
                         do { curDate = new Date();
                              console.log('TEMPO'); }
                         while(curDate-date < 3000);
                         document.getElementById('caption').innerHTML='Zipando, aguarde...';
                         var zip= window.open("/webtiger/downloads/zip?NameDir="+document.getElementById('NameDir').value+"&downloadToken="+document.getElementById('downloadToken').value, "_blank"); 
                         zip.document.body.innerHTML = "<p><b>Zipando arquivos. Não feche essa janela</b></p>";
                       }
                      }
                    });
                  i++;
                  }
                }
              });
            }
          });
        }
      }
      }
    });
   }     
  }

function qtoCheckboxesChecked(source){
 var checkboxes= document.getElementsByName("checkbox");
 vetor= (document.forms['nextPage'].elements["quaisCheckboxes"].value).split(" ");  
 //console.log('Vetor:'+vetor);

 if (source.checked==false) 
  checkboxTotalUnchecked();   
  
 for(var i=0; i< checkboxes.length; i++) {
      checkboxes[i].checked = source.checked;
      if (source.checked) {
         if (! (vetor).includes (checkboxes[i].value) ){
            console.log('entrou:'+checkboxes[i].value);
            document.forms['nextPage'].elements["quaisCheckboxes"].value= document.forms['nextPage'].elements["quaisCheckboxes"].value+checkboxes[i].value+' ';
          }
        }
      else {
        console.log('DESMARCAR:'+checkboxes[i].value);
        vetor= (document.forms['nextPage'].elements["quaisCheckboxes"].value).split(" ");  
        if ((vetor).includes (checkboxes[i].value) ) {
          var index = vetor.indexOf(checkboxes[i].value);
          vetor.splice(index, 1);
          document.forms['nextPage'].elements["quaisCheckboxes"].value=vetor.join(" ");
          console.log('FINAL:'+document.forms['nextPage'].elements["quaisCheckboxes"].value);
        }
       }
  }

  console.log('MARCANDO TODOS:'+document.forms['nextPage'].elements["quaisCheckboxes"].value);
  document.forms['previousPage'].elements["quaisCheckboxes"].value= document.forms['nextPage'].elements["quaisCheckboxes"].value;
  document.forms['firstPage'].elements["quaisCheckboxes"].value= document.forms['nextPage'].elements["quaisCheckboxes"].value;
  document.forms['lastPage'].elements["quaisCheckboxes"].value= document.forms['nextPage'].elements["quaisCheckboxes"].value;  
  document.getElementById("quaisCheckboxes").value= document.forms['nextPage'].elements["quaisCheckboxes"].value;  
}

function sumChecked(source){
  console.log('Pass:'+document.getElementById('passCheckboxes').value);
  if (source.checked){
    document.forms['nextPage'].elements["quaisCheckboxes"].value= document.forms['nextPage'].elements["quaisCheckboxes"].value+source.value+' ';
    console.log('nextPage:'+document.forms['nextPage'].elements["quaisCheckboxes"].value);

    flag = true;
    for (i=0; i<document.getElementsByName('checkbox').length; i++){ 
     console.log('TOTAL SOMA:'+ (document.getElementsByName('checkbox')[i].value+':'+document.getElementsByName('checkbox')[i].checked) );
     if (document.getElementsByName('checkbox')[i].checked==false)
      flag=false;
  }
    if (flag==true)
      document.getElementById('checkboxParcial').checked=true;

   }
  else{
    vetor= (document.forms['nextPage'].elements["quaisCheckboxes"].value).split(" ");  
    if ((vetor).includes (source.value) ) {
      var index = vetor.indexOf(source.value);
      vetor.splice(index, 1);
      document.forms['nextPage'].elements["quaisCheckboxes"].value=vetor.join(" ");
      console.log('FINAL SOMA:'+document.forms['nextPage'].elements["quaisCheckboxes"].value);
    }
    document.getElementById('checkboxParcial').checked=false;
    checkboxTotalUnchecked(); 

  }

    document.forms['previousPage'].elements["quaisCheckboxes"].value= document.forms['nextPage'].elements["quaisCheckboxes"].value;
    document.forms['firstPage'].elements["quaisCheckboxes"].value= document.forms['nextPage'].elements["quaisCheckboxes"].value;
    document.forms['lastPage'].elements["quaisCheckboxes"].value= document.forms['nextPage'].elements["quaisCheckboxes"].value;
    document.getElementById("quaisCheckboxes").value= document.forms['nextPage'].elements["quaisCheckboxes"].value; 

    console.log(document.forms['nextPage'].elements["quaisCheckboxes"].value);
}

function ChangingTarget() {
   $.ajax({
    type: "POST",
    url: "carregamentoAlvo",
    data: JSON.stringify({'opr':document.getElementById('operation').value}),
    contentType: 'application/json;charset=UTF-8',
   success: function (data) {
    console.log(data);
    if (data['target']==false && typeof(data['target'])=='boolean')
      alert('Erro de carregamento de opções no Alvo');
    else {
      var selectOpt = document.getElementById('target');
      $('#target').empty();

      var option = document.createElement('option');
      option.value ='todos';
      option.text='---Todos---';
      selectOpt.add(option, 0); 

      for (i=0; i< data['target'].length; i++) {
          var option = document.createElement('option');

          if (data['target'][i]['tel']!= null) 
            option.appendChild( document.createTextNode(data['target'][i]['nom']+' - ('+data['target'][i]['ddd']+') '+data['target'][i]['tel'] ));
          else 
            option.appendChild( document.createTextNode(data['target'][i]['nom']+' - ()'));
          
            option.value = data['target'][i]['cod']; 
            selectOpt.add(option, (i+1)); 
            console.log('insere: '+data['target'][i]['nom']);
      }
      selectOpt.selectedIndex = 0;
    }
  }
   });
}

function verifyIntervalDate(){
   var dateInitial= document.getElementById('initialDate').value;
   var dateFinal= document.getElementById('endDate').value;

   if (dateInitial!='' & dateFinal!=''){
      var diferenca = new Date (dateFinal).getTime() - new Date (dateInitial).getTime();
      if (diferenca <0) {
        alert('Data Inicial deve ser menor que data final'); 
        document.getElementById('downloadButton').disabled = true;
        document.getElementById('downloadButton').style.background= '#DDDDDD';
      }
      else {
        document.getElementById('downloadButton').disabled = false;
        document.getElementById('downloadButton').style.background= '#4CAF50';
      }
   }
  }

function verifyHour(){
   var initialHour= document.getElementById('initialHour').value;
   var endHour= document.getElementById('endHour').value;
   var dateInitial= document.getElementById('initialDate').value;
   var dateFinal= document.getElementById('endDate').value;
   var diferenca = new Date (dateFinal).getTime() - new Date (dateInitial).getTime();

   if (initialHour!='' & endHour!=''){
        endHour = endHour.split(":");
        initialHour = initialHour.split(":");

        if (diferenca ==0) {
           var hour = new Date (2000, 0 , 1, 9, endHour[0], endHour[1]).getTime() - new Date (2000, 0 , 1, 9, initialHour[0], initialHour[1]).getTime();   
           if (hour <0){
            alert('A Hora Inicial deve ser menor que a Hora Final');
            document.getElementById('downloadButton').disabled = true;
            document.getElementById('downloadButton').style.background= '#DDDDDD';
          }
            else{
              document.getElementById('downloadButton').disabled = false;
              document.getElementById('downloadButton').style.background= '#4CAF50';
            }
         }
      }
}

function verifyTranscription(){
  var transcription= document.getElementById('transcription').value;
  if (transcription == 'transcritas')
     document.getElementById('transcriptionPart').disabled = false;
   else {
    document.getElementById('transcriptionPart').disabled = true;
    document.getElementById('transcriptionPart').value='';
  }
}

function verifySinopse(){
  var sinopse= document.getElementById('sinopse').value;
  if (sinopse == 'comSinopse')
     document.getElementById('sinopsePart').disabled = false;
   else {
    document.getElementById('sinopsePart').disabled = true;
    document.getElementById('sinopsePart').value='';
  }
}

function mascara(numero, mask, tipo){
  var i = numero.value.length;
  if (i==4)
    numero.value = numero.value+ mask.substring(0,1);
}

 function HiddenFieldInitialHour(){ document.getElementById('initialHourHidden').value = document.getElementById('initialHour').value; }
  function HiddenFieldEndHour(){ document.getElementById('endHourHidden').value = document.getElementById('endHour').value; }
   function HiddenTranscriptionPart(){ document.getElementById('transcriptionPartHidden').value = document.getElementById('transcriptionPart').value; }
    function HiddenSinopsePart(){ document.getElementById('sinopsePartHidden').value = document.getElementById('sinopsePart').value; }

//========================================================================================================================================

function checkboxTotalAction(source){
  window.stop();
  if (source.checked) {
    document.getElementById('checkboxParcial').checked=true; 
    var checkboxes= document.getElementsByName("checkbox");
    document.forms['nextPage'].elements["checkBoxTotalHidden"].value= 'checked';
    document.forms['previousPage'].elements["checkBoxTotalHidden"].value= 'checked';
    document.forms['firstPage'].elements["checkBoxTotalHidden"].value= 'checked';
    document.forms['lastPage'].elements["checkBoxTotalHidden"].value= 'checked';

    for(var i=0; i< checkboxes.length; i++) 
      checkboxes[i].checked = source.checked;

    rawQuery= document.forms['nextPage'].elements["rawQuery"].value;
    //desabilitando botoes
    disableButtons(true);
    document.getElementById('littleLoading').style.display='inline-block';
    $.ajax({
            type: "POST",
            url: "checkboxAll",
            data: JSON.stringify({ 'rawQuery': rawQuery }),
            contentType: 'application/json;charset=UTF-8',
            success: function (data) {
               document.forms['nextPage'].elements["quaisCheckboxes"].value= data;
               document.forms['previousPage'].elements["quaisCheckboxes"].value= document.forms['nextPage'].elements["quaisCheckboxes"].value;
               document.forms['firstPage'].elements["quaisCheckboxes"].value= document.forms['nextPage'].elements["quaisCheckboxes"].value;
               document.forms['lastPage'].elements["quaisCheckboxes"].value= document.forms['nextPage'].elements["quaisCheckboxes"].value;  
               document.getElementById("quaisCheckboxes").value= document.forms['nextPage'].elements["quaisCheckboxes"].value; 
               //console.log(document.forms['nextPage'].elements["quaisCheckboxes"].value);
               document.getElementById('littleLoading').style.display='none';
               disableButtons(false);
            }});

    
  }
  else {
    document.getElementById('checkboxParcial').checked=false; 
    document.getElementById('passCheckboxes').value='';
    qtoCheckboxesChecked(document.getElementById('checkboxParcial'));
    document.forms['nextPage'].elements["quaisCheckboxes"].value= '';
    document.forms['previousPage'].elements["quaisCheckboxes"].value= document.forms['nextPage'].elements["quaisCheckboxes"].value;
    document.forms['firstPage'].elements["quaisCheckboxes"].value= document.forms['nextPage'].elements["quaisCheckboxes"].value;
    document.forms['lastPage'].elements["quaisCheckboxes"].value= document.forms['nextPage'].elements["quaisCheckboxes"].value; 

    document.forms['nextPage'].elements["checkBoxTotalHidden"].value= '';
    document.forms['previousPage'].elements["checkBoxTotalHidden"].value= '';
    document.forms['firstPage'].elements["checkBoxTotalHidden"].value= '';
    document.forms['lastPage'].elements["checkBoxTotalHidden"].value= '';  
  } 
}

function checkboxTotalUnchecked(){
    document.getElementById('checkboxTotal').checked=false;
    document.forms['nextPage'].elements["checkBoxTotalHidden"].value= '';
    document.forms['previousPage'].elements["checkBoxTotalHidden"].value= '';
    document.forms['firstPage'].elements["checkBoxTotalHidden"].value= '';
    document.forms['lastPage'].elements["checkBoxTotalHidden"].value= ''; 
}

function disableButtons(disable){
    if (document.forms['nextPage'].elements["nextPageButton"]){
      if (disable ==true){
        document.forms['nextPage'].elements["nextPageButton"].setAttribute("disabled",true);
        document.forms['nextPage'].elements["nextPageButton"].setAttribute("style", "background-color: #e3e3e4;");
      }
      else{
        document.forms['nextPage'].elements["nextPageButton"].removeAttribute("disabled");
        document.forms['nextPage'].elements["nextPageButton"].setAttribute("style", "background-color: #4CAF50;");
      }
    }

    if (document.forms['previousPage'].elements["previousPageButton"]){
      if (disable ==true){
        document.forms['previousPage'].elements["previousPageButton"].setAttribute("disabled",true);
        document.forms['previousPage'].elements["previousPageButton"].setAttribute("style", "background-color: #e3e3e4;");
      }
      else{
        document.forms['previousPage'].elements["previousPageButton"].removeAttribute("disabled");
        document.forms['previousPage'].elements["previousPageButton"].setAttribute("style", "background-color: #4CAF50;");
      }
    }

    if (document.forms['lastPage'].elements["lastPageButton"]){
      if (disable ==true){
        document.forms['lastPage'].elements["lastPageButton"].setAttribute("disabled",true);
        document.forms['lastPage'].elements["lastPageButton"].setAttribute("style", "background-color: #e3e3e4;");
      }
      else{
        document.forms['lastPage'].elements["lastPageButton"].removeAttribute("disabled");
        document.forms['lastPage'].elements["lastPageButton"].setAttribute("style", "background-color: #4CAF50;");
      }
    }

    if (document.forms['firstPage'].elements["firstPageButton"]){
      if (disable ==true){
        document.forms['firstPage'].elements["firstPageButton"].setAttribute("disabled",true);
        document.forms['firstPage'].elements["firstPageButton"].setAttribute("style", "background-color: #e3e3e4;");
      }
      else{
        document.forms['firstPage'].elements["firstPageButton"].removeAttribute("disabled");
        document.forms['firstPage'].elements["firstPageButton"].setAttribute("style", "background-color: #4CAF50;");
      }
    }

    if (disable ==true){    
      document.getElementById("download").setAttribute("disabled",true);
      document.getElementById("download").setAttribute("style", "background-color: #e3e3e4;");
    }
    else {
      document.getElementById("download").removeAttribute("disabled");
      document.getElementById("download").setAttribute("style", "background-color: #4CAF50;");
    }
}