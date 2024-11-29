// 获取按钮的 data-url 属性值
const baseUrl = window.location.origin;
const url_label_light_set = `${baseUrl}/ptl/label_light_set`;
const url_label_info_get = `${baseUrl}/ptl/label_info_get`;
const url_label_rst = `${baseUrl}/ptl/label_rst`;
const url_ip_addr_set = `${baseUrl}/ptl/ip_addr_set`;
const url_ip_port_set = `${baseUrl}/ptl/ip_port_set`;
const url_ip_addr_get = `${baseUrl}/ptl/ip_addr_get`;
const url_ip_port_get = `${baseUrl}/ptl/ip_port_get`;
const url_sys_rst = `${baseUrl}/ptl/sys_rst`;
const url_sys_default_set = `${baseUrl}/ptl/sys_default_set`;

document.addEventListener('DOMContentLoaded', () => {
    // 获取所有的 radio 按钮
    const nodeTypeRadios = document.querySelectorAll('input[name="node_type"]');

    // 为所有 radio 按钮添加事件监听
    nodeTypeRadios.forEach(radio => {
        radio.addEventListener('change', function (event) {
            // 找到当前 radio 按钮所在的 form
            const form = event.target.closest('form');
            if (!form) return; // 如果找不到 form，则退出

            // 找到 form 内的 groupDiv 和 nodeFormsetDiv
            const groupDiv = form.querySelector('[id^="group"]');
            const nodeFormsetDiv = form.querySelector('[id^="node-formset"]');

            if (!groupDiv || !nodeFormsetDiv) return; // 如果找不到目标元素，则退出

            // 根据当前 radio 的值切换显示/隐藏
            if (this.value === 'NET_LABLE_TOTAL') {
                groupDiv.style.display = 'block';
                nodeFormsetDiv.style.display = 'none';
            } else {
                groupDiv.style.display = 'none';
                nodeFormsetDiv.style.display = 'block';
            }
        });
    });

    // 绑定提交按钮事件
    $('#label_light_set_button').click(function () {
        event.preventDefault();
        const formData = $('#label_light_set_form').serialize();
        // 发送 AJAX 请求
        $.ajax({
            url: url_label_light_set,
            method: "GET",
            data: formData,
            success: function (response) {
                console.log(response);
                // 动态更新页面内容
                $('#response_area').html(
                    `<p>Status: ${response.status}</p>
                         <p>Packet: ${response.packet}</p>`
                );
            },
            error: function () {
                console.log("请求失败！");
                $('#response_area').html("<p>请求失败，请重试！</p>");
            }
        });
    });

    $('#label_info_get_button').click(function () {
        event.preventDefault();
        // 获取表单数据
        const formData = $('#label_info_get_form').serialize();

        // 发送 AJAX 请求
        $.ajax({
            url: url_label_info_get,
            method: "GET",
            data: formData,
            success: function (response) {
                console.log(response);
                // 动态更新页面内容
                $('#response_area').html(
                    `<p>Status: ${response.status}</p>
                         <p>Packet: ${response.packet}</p>`
                );
            },
            error: function () {
                console.log("请求失败！");
                $('#response_area').html("<p>请求失败，请重试！</p>");
            }
        });
    });

    $('#label_rst_button').click(function () {
        event.preventDefault();
        // 获取表单数据
        const formData = $('#label_rst_form').serialize();

        // 发送 AJAX 请求
        $.ajax({
            url: url_label_rst,
            method: "GET",
            data: formData,
            success: function (response) {
                console.log(response);
                // 动态更新页面内容
                $('#response_area').html(
                    `<p>Status: ${response.status}</p>
                         <p>Packet: ${response.packet}</p>`
                );
            },
            error: function () {
                console.log("请求失败！");
                $('#response_area').html("<p>请求失败，请重试！</p>");
            }
        });
    });

    $('#ip_addr_set_button').click(function () {
        event.preventDefault();
        // 获取表单数据
        const formData = $('#ip_addr_set_form').serialize();

        // 发送 AJAX 请求
        $.ajax({
            url: url_ip_addr_set,
            method: "GET",
            data: formData,
            success: function (response) {
                console.log(response);
                // 动态更新页面内容
                $('#response_area').html(
                    `<p>Status: ${response.status}</p>
                         <p>Packet: ${response.packet}</p>`
                );
            },
            error: function () {
                console.log("请求失败！");
                $('#response_area').html("<p>请求失败，请重试！</p>");
            }
        });
    });

    $('#ip_port_set_button').click(function () {
        event.preventDefault();
        // 获取表单数据
        const formData = $('#ip_port_set_form').serialize();

        // 发送 AJAX 请求
        $.ajax({
            url: url_ip_port_set,
            method: "GET",
            data: formData,
            success: function (response) {
                console.log(response);
                // 动态更新页面内容
                $('#response_area').html(
                    `<p>Status: ${response.status}</p>
                         <p>Packet: ${response.packet}</p>`
                );
            },
            error: function () {
                console.log("请求失败！");
                $('#response_area').html("<p>请求失败，请重试！</p>");
            }
        });
    });

    $('#ip_addr_get_button').click(function () {
        event.preventDefault();
        formdata = '';

        // 发送 AJAX 请求
        $.ajax({
            url: url_ip_addr_get,
            method: "GET",
            data: formdata,
            success: function (response) {
                console.log(response);
                // 动态更新页面内容
                $('#response_area').html(
                    `<p>Status: ${response.status}</p>
                         <p>Packet: ${response.packet}</p>`
                );
            },
            error: function () {
                console.log("请求失败！");
                $('#response_area').html("<p>请求失败，请重试！</p>");
            }
        });
    });

    $('#ip_port_get_button').click(function () {
        event.preventDefault();
        formdata = '';

        // 发送 AJAX 请求
        $.ajax({
            url: url_ip_port_get,
            method: "GET",
            data: formdata,
            success: function (response) {
                console.log(response);
                // 动态更新页面内容
                $('#response_area').html(
                    `<p>Status: ${response.status}</p>
                         <p>Packet: ${response.packet}</p>`
                );
            },
            error: function () {
                console.log("请求失败！");
                $('#response_area').html("<p>请求失败，请重试！</p>");
            }
        });
    });

    $('#sys_rst_button').click(function () {
        event.preventDefault();
        formdata = '';

        // 发送 AJAX 请求
        $.ajax({
            url: url_sys_rst,
            method: "GET",
            data: formdata,
            success: function (response) {
                console.log(response);
                // 动态更新页面内容
                $('#response_area').html(
                    `<p>Status: ${response.status}</p>
                         <p>Packet: ${response.packet}</p>`
                );
            },
            error: function () {
                console.log("请求失败！");
                $('#response_area').html("<p>请求失败，请重试！</p>");
            }
        });
    });

    $('#sys_default_set_button').click(function () {
        event.preventDefault();
        formdata = '';

        // 发送 AJAX 请求
        $.ajax({
            url: url_sys_default_set,
            method: "GET",
            data: formdata,
            success: function (response) {
                console.log(response);
                // 动态更新页面内容
                $('#response_area').html(
                    `<p>Status: ${response.status}</p>
                         <p>Packet: ${response.packet}</p>`
                );
            },
            error: function () {
                console.log("请求失败！");
                $('#response_area').html("<p>请求失败，请重试！</p>");
            }
        });
    });
});
