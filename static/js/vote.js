var Vote = {
    init: function () {
        this.$container = $('.container.main-section.border')
        this.render();
        this.bindEvents();
    },

    render: function () {

    },

    bindEvents: function () {
        $('.upvote', this.$container).on('click', function (e) {
            e.preventDefault();
            var self = $(this);
            var url = $(this).attr('href');
            $.ajax(
                {
                    type:"GET",
                    url:url,
                    success: function (data) {
                        $('#votes_count'+ data['id']).text(data['votes']);
                        $('.fa-chevron-up', self).toggleClass('active');

                    }
                }
            );
            return false;
        });

        $('.downvote', this.$container).on('click', function (e) {
            e.preventDefault();
            var self = $(this);
            var url = $(this).attr('href');
            $.ajax(
                {
                    type:"GET",
                    url:url,
                    success: function (data) {
                        $('#votes_count'+ data['id']).text(data['votes']);
                        $('.fa-chevron-down', self).toggleClass('active');
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