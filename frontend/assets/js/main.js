let app = {

    animalPage: {
        renderSchedule: function(schedule) {
            for (let i in schedule) {
                let item = schedule[i];
                let time = item.time.split(':');
                app.animalPage.addScheduleItem(item.id, time[0], time[1], item.portions)
            }
        },

        addScheduleItem: function (id, m, s, portions) {
            let template = $("#schedule_item").html();

            template = template.replace(/\{1\}/g, id === undefined ? '' : id);
            template = template.replace(/\{2\}/, m === undefined ? '' : m);
            template = template.replace(/\{3\}/, s === undefined ? '' : s);
            template = template.replace(/\{4\}/, portions === undefined ? '' : portions);

            $("#animal_schedule").append(template);
        },

        removeScheduleItem: function(obj) {
            let fieldset = $(obj).parent().parent().parent();
            let scheduleId = fieldset.data('id');
            if (scheduleId != '') {
               app.removeAnimalSchedule(scheduleId);
            }

            fieldset.remove();
        },

        saveSchedule: function() {
            let schedule = [];
            $("#animal_schedule .schedule-item").each(function() {
                let scheduleId = $(this).data('id');
                let inputs = $(this).find('input');

                schedule.push({
                    id: scheduleId,
                    time: inputs[0].value + ':' + inputs[1].value,
                    portions: inputs[2].value
                })
            });

            if (schedule.length !== 0) {
                app.updateAnimalSchedule(schedule, () => {
                    app.showAnimalPage(app.getAnimalId());
                })
            }
        }
    },

    getAnimalId: function() {
        return localStorage.getItem('animal');
    },

    init: function() {
        let animalId = app.getAnimalId();
        if (animalId !== null) {
            app.showAnimalPage(animalId);
        } else {
            app.showAnimalCreatePage();
        }
    },

    showAnimalPage: function(animalId) {
        app.getAnimalInfo(animalId, (response) => {
            app.showPage('animal_view', () => {
                // set name
                $("#animal_name").text(response.info.name);
                app.animalPage.renderSchedule(response.schedule)
            })
        })
    },

    handleGotoAnimal: function() {
        let animalId = $("#animals_select").val();
        if (animalId != '') {
            app.savePrefferedAnimal(animalId);
            app.showAnimalPage(animalId);
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
            })
        })
    },

    handleCreateAnimal: function() {
        let name = $("#animal-name").val();
        app.createAnimal(name, (response) => {
            if (response.status !== 200) {
                alert(response.responseJSON.error);
            } else {
                app.savePrefferedAnimal(response.responseJSON.id);
                app.showAnimalPage(response.responseJSON.id);
            }
        });
    },

    savePrefferedAnimal: function(animalId) {
        localStorage.setItem('animal', animalId);
    },

    showPage: function(pageId, callback) {
        $("#app").fadeOut(500, function() {
            $("#app").html($("#" + pageId).html());
            if (callback !== undefined) {
                callback();
            }
            $("#app").fadeIn(500);
        })
    },

    getAnimalsList: function(callback) {
        $.get('/animal', function(response) {
            callback(response)
        }, 'json')
    },

    getAnimalInfo: function(id, callback) {
        $.get('/animal/' + id, function(response) {
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
    },

    removeAnimalSchedule: function(id) {
        $.ajax({
            type: 'DELETE',
            url: '/schedule/' + id,
            dataType: 'json',
            contentType: 'application/json'
        })
    },

    updateAnimalSchedule: function(schedule, callback) {
        $.ajax({
            type: 'PUT',
            url: '/animal/' + app.getAnimalId() + '/schedule',
            dataType: 'json',
            data: JSON.stringify(schedule),
            contentType: 'application/json',
            complete: callback
        })
    }
};

app.init();