$( document ).ready(function() {
  i=0;
cartvalue = document.getElementById('cart').innerHTML;
});

function itemtoadd(id) {
  item = []
  item[0] = document.getElementById('name'+id).innerHTML;
  item[1] = document.getElementById('size'+id).innerHTML;
  item[2] = document.getElementById('price'+id).innerHTML;
  addtocart(item);
  }
var list = [];
function addtocart(item){
  i++;
  document.getElementById('cart').innerHTML = cartvalue+ '(' + i + ')';
  list.push({"name":item[0],"size":item[1],"price":item[2]});
  }
function displaycart(){
  $("#container").empty();
  console.dir(list);
  for(i=0;i<list.length;i++){
  $("#container").append("<p>"+list[i].name+"</p>" + "<p>" + list[i].size + "</p>" + "<p>" + list[i].price + "</p><br/>" );
    }
  $("#cartlist").toggleClass("hidden");
  }


