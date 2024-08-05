/** @odoo-module */

import { registry } from "@web/core/registry"
import { PhoneField } from "@web/views/fields/phone/phone_field";

class FormTelegramField extends PhoneField {
    setup(){
        super.setup()
    }

    get telegramHref() {
        const phoneNumber = this.props.value.replace(/\D/g, '');
        if (phoneNumber.startsWith('7')) {
            return `https://t.me/+${phoneNumber}`;
        } else if (phoneNumber.startsWith('8')) {
            return `https://t.me/+7${phoneNumber.slice(1)}`;
        } else if (phoneNumber.length === 10) {
            return `https://t.me/+7${phoneNumber}`;
        } else {
            return '';
        }
    }

}

FormTelegramField.template = "owl.FormTelegramField"

registry.category("fields").add("telegram", FormTelegramField)
