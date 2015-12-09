    (function($){
        $(document).ready(function () {
        $(".related-widget-wrapper:has(table)").addClass('related-widget-wrapper-user-permissions');
        $('#perm_add_select_all').on('change', function () {
            var state = $(this).prop('checked');
            $('#tabular_permissions').find('tr td.add').find('input').each(function (i, e) {
                $(e).prop('checked', state)
            })
        });
        $('#perm_change_select_all').on('change', function () {
            var state = $(this).prop('checked');
            $('#tabular_permissions').find('tr td.change').find('input').each(function (i, e) {
                $(e).prop('checked', state)
            })
        });
        $('#perm_delete_select_all').on('change', function () {
            var state = $(this).prop('checked');
            $('#tabular_permissions').find('tr td.delete').find('input').each(function (i, e) {
                $(e).prop('checked', state)
            })
        });
        $('form').on('submit', function () {
            var user_perms = [];
            $('#tabular_permissions').find("input[type=checkbox]").not('.select-all').each(function (i, elem) {
                var $elem = $(elem);
                if ($(elem).prop('checked')) {
                    user_perms.push($elem.attr('data-perm-id'))
                }
            });
            var user_permissions = $('[name=user_permissions]');
            var output = [];
            $.each(user_perms, function (key, value) {
                output.push('<option value="' + value + '" selected="selected" style="display:none"></option>');
            });
            user_permissions.append(output);
        })
    });
    })(django.jQuery);
