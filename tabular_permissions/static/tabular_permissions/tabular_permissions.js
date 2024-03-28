'use strict';
{
    window.addEventListener('load', function(e) {

        // Look for view select all
        const perm_view_select_all = this.document.getElementById('perm_view_select_all');
        perm_view_select_all.addEventListener('change', function(){
            const state = this.checked;
            const perm_inputs = document.getElementById("tabular_permissions").querySelectorAll("td.view");
            perm_inputs.forEach(element => {
                element.getElementsByTagName("input")[0].checked = state;
            });
        });

        // Look for add select all
        const perm_add_select_all = this.document.getElementById('perm_add_select_all');
        perm_add_select_all.addEventListener('change', function(){
            const state = this.checked;
            const perm_inputs = document.getElementById("tabular_permissions").querySelectorAll("td.add");
            perm_inputs.forEach(element => {
                element.getElementsByTagName("input")[0].checked = state;
            });
        }); 

        // Look for change select all
        const perm_change_select_all = this.document.getElementById('perm_change_select_all');
        perm_change_select_all.addEventListener('change', function(){
            const state = this.checked;
            const perm_inputs = document.getElementById("tabular_permissions").querySelectorAll("td.change");
            perm_inputs.forEach(element => {
                element.getElementsByTagName("input")[0].checked = state;
            });
        });

        // Look for change select all
        const perm_delete_select_all = document.getElementById('perm_delete_select_all');
        perm_delete_select_all.addEventListener('change', function(){
            const state = this.checked;
            const perm_inputs = document.getElementById("tabular_permissions").querySelectorAll("td.delete");
            perm_inputs.forEach(element => {
                element.getElementsByTagName("input")[0].checked = state;
            });
        });

        // Look for select all in row
        const select_all_row = this.document.querySelectorAll(".select-all.select-row");
        select_all_row.forEach(input => {
            input.addEventListener('change', function(){
                const tr_parent = this.parentElement.parentElement.parentElement;
                const checkboxes = tr_parent.querySelectorAll("input.checkbox:not(.select-all)");

                checkboxes.forEach(element => {
                    element.checked = this.checked;
                });
            });
        });

        // Submit form 
        const form = this.document.querySelectorAll("form:not(#logout-form)")[0];
        
        form.addEventListener('submit', function(){
            const user_perms = [];
            const table_permissions = document.getElementById("tabular_permissions");
            const input_name = table_permissions.getAttribute("data-input-name");
            
            
            table_permissions.querySelectorAll("input[type=checkbox]:not(.select-all)").forEach(element => {
                if(element.checked){
                    user_perms.push(element.getAttribute("data-perm-id"));
                }
            });
            
            const user_group_permissions = document.querySelector('[name=' + input_name + ']');
            Object.entries(user_perms).forEach(entry => {
                const [key, value] = entry;
                user_group_permissions.insertAdjacentHTML('beforeend',
                '<option value="' + value + '" selected="selected" style="display:none"></option>')
            });
        });

    });
}