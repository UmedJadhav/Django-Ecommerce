$(document).ready(function(){

  const contactForm = $('.contact-form')
  const contactFormMethod =  contactForm.attr('method')

  function displaySubmitting(submitBtn, defaultText, doSubmit){
    if(doSubmit){
      submitBtn.addClass('disabled')  
      submitBtn.html("<i class='fa fa-spin fa-spinner'></i>  Submitting...")    
    }else{
      submitBtn.removeClass('disabled')
      submitBtn.html(defaultText)
    }
  }

  contactForm.submit(function(event){
    const contactFormEndpoint =  contactForm.attr('action')
    const contactButtonSubmitBtn = contactForm.find("[type='submit']")
    const contactButtonSubmitBtnTxt = contactButtonSubmitBtn.text()
    event.preventDefault();
    const contactFormdata = contactForm.serialize()
    displaySubmitting(contactButtonSubmitBtn,'',true)
    $.ajax({
      method: contactFormMethod,
      url: contactFormEndpoint,
      data: contactFormdata,
      success: function(data){
        contactForm[0].reset() // clears the form
        $.alert({
            title: 'Success!',
            content: data.message,
            theme: 'modern'
          })
        
        setTimeout(displaySubmitting(contactButtonSubmitBtn, contactButtonSubmitBtnTxt, false),500);
      }
      ,
      error(errorData){
        console.log(errorData)
        let errormsg = ''
        $.each(errorData.responseJSON, function(key, value){
          errormsg += `${key}:${value[0].message}`
        })

        $.alert({
            title: 'Oops!',
            content: errormsg,
            theme: 'modern'
          })
        
          setTimeout(displaySubmitting(contactButtonSubmitBtn, contactButtonSubmitBtnTxt, false),500);
      }
    });
  });

  const searchForm = $('.search-form')
  const searchInput = searchForm.find("[name='q']")
  let typingTimer ;
  const typingInterval = 500
  const searchBtn = searchForm.find("[type='submit']")
  searchInput.keyup(function(event){
    clearTimeout(typingTimer);
    typingTimer = setTimeout(performSearch,typingInterval)
  })

  searchInput.keydown(function(){
    clearTimeout(typingTimer);
  })

  function displaySearching(){
    searchBtn.addClass('disabled')  
    searchBtn.html("<i class='fa fa-spin fa-spinner'></i>  Searching...")       
  }

  function performSearch(){
    displaySearching()
    const query = searchInput.val()
    setTimeout(function(){
    window.location.href = `/search/?q=${query}`
    },1000)
  }

  let prodcutForm = $('.form-product-add-ajax')
  prodcutForm.submit(function(event){
    event.preventDefault();
    const thisForm = $(this);
    // const actionEndpoint = thisForm.attr('action');
    const actionEndpoint = thisForm.attr('data-endpoint');
    const httpMethod = thisForm.attr('method');
    const formData = thisForm.serialize();
    $.ajax({
      url: actionEndpoint,
      method: httpMethod,
      data: formData,
      success: function(data){
        const submitSpan = thisForm.find('.submit-span');
        if(data.added){
          submitSpan.html("In Cart <button type='submit' class='btn btn-link'>Remove ?</button>");
        }else{
          submitSpan.html("<button type='submit' class='btn btn-success'>Add to Cart</button>");
        }

        const navbarCount = $('.navbar-cart-count')
        navbarCount.text(data.cartItemCount);
        const currentUrl = window.location.href;
        if(currentUrl.indexOf('cart') != -1){
          refreshCart();
        } 
      },
      error: function(errorData){
        $.alert({
            title: 'Oops!',
            content: 'An error occured',
            theme: 'modern'
          })
      }
    });
  })

  function refreshCart(){
    const cartTable = $('.cart-table');
    const cartBody = cartTable.find('.cart-body');
    const productRows = cartBody.find('cart-product');
    const currentUrl = window.location.href;
    const refreshCartUrl = '/api/cart/';
    const refreshCartMethod = 'GET';
    $.ajax({
      url: refreshCartUrl,
      method: refreshCartMethod,
      data: {},
      success: function(data){
        console.log('successRefresh');
        console.log(data);
        let hiddenCartItemRemovedForm = $('.cart-item-remove-form')
        if(data.products.lenght > 0){
          productRows.html(" ")
          i=data.products.lenght;
          $.each(data.products, function(index, value){
            console.log(value);
            let newCartItemRemove = hiddenCartItemRemovedForm.clone()
            newCartItemRemove.css('display','block')
            // newCartItemRemove.removeClass('hidden-class')
            newCartItemRemove.find('.cart-item-product-id').val(value.id )
            cartBody.prepend(`<tr><th scope="row">${i}</th><td><a href='${value.url}'>${value.name}</a>${newCartItemRemove.htm()}</td><td>${value.price}</td></tr>`);
            i--
          });
          // productRows.html("<tr><td colspan=3>Coming Soon</td></tr>");
          cartBody.find('.cart-subtotal').text(data.subtotal);
          cartBody.find('.cart-total').text(data.total);
        }else{
          window.location.href = currentUrl;
        }
      },
      error: function(errorData){
        $.alert({
            title: 'Oops!',
            content: 'An error occured',
            theme: 'modern'
          })
      }
    });
  }
})