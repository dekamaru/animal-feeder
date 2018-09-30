let app = {

    init: function() {
        app.showLoader();

        let animalId = localStorage.getItem('animal');
        if (animalId !== null) {

        } else {
            app.showAnimalCreatePage();
        }
    },

    showAnimalCreatePage: function() {
        app.getAnimalsList((data) => {

            app.showPage('no_animals_screen', () => {
                if (data.length === 0) {
                    $("#select-existing-animal").hide();
                } else {
                    let animals_select = $("#animals_select");
                    animals_select.html('<option disabled selected>Питомец</option>');
                    for (let i in data) {
                        animals_select.append('<option value="'+ data[i].id +'">'+ data[i].name +'</option>');
                    }
                    $("#select-existing-animal").show();
                }

                app.hideLoader();
            })
        })
    },

    handleCreateAnimal: function() {
        app.showLoader();

        let name = $("#animal-name").val();
        app.createAnimal(name, (response) => {
            if (response.status !== 200) {
                // error
                $("#animal-name-invalid-feedback").text(response.responseJSON.error);
                $("#animal-name").addClass('is-invalid')
            } else {
                // save data and go to next page
            }
            app.hideLoader();
        });
    },

    showLoader: function() {
        $("#app").fadeOut(200, function() {
            $(".loader").fadeIn(200);
        });

    },

    hideLoader: function() {
        $(".loader").fadeOut(200, function () {
            $("#app").fadeIn(200);
        });
    },

    showPage: function(pageId, callback) {
        $("#app").fadeOut(200, function() {
            $("#app").html($("#" + pageId).html());
            if (callback !== undefined) {
                callback();
            }
            $("#app").fadeIn(200);
        })
    },

    getAnimalsList: function(callback) {
        $.get('/animal', function(response) {
            callback(response)
        }, 'json')
    },

    createAnimal: function(name, callback) {
        $.ajax({
            type: 'post',
            url: '/animal',
            dataType: 'json',
            data: JSON.stringify({name: name}),
            contentType: 'application/json',
            complete: callback
        })
    }
};

app.init();