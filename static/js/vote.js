var Vote = {
    init: function () {
        this.$container = $('.container.main-section.border')
        this.render();
        this.bindEvents();
    },

    render: function () {

    },

    bindEvents: function () {
        $('.fa.fa-chevron-up', this.$container).on('click', function (e) {
            e.preventDefault();
            var url = $(this).attr('href');
            $.ajax(
                {
                    type:"GET",
                    url:url,
                    success: function (data) {
                        $('#votes_count'+ data['id']).text(data['votes']);

                    }
                }
            );
            return false;
        });

        $('.fa.fa-chevron-down', this.$container).on('click', function (e) {
            e.preventDefault();
            var url = $(this).attr('href');
            $.ajax(
                {
                    type:"GET",
                    url:url,
                    success: function (data) {
                        $('#votes_count'+ data['id']).text(data['votes']);

                    }
                }
            );
            return false;
        });
    }
};

$(document).ready(function () {
    Vote.init();
});