/** @odoo-module **/

import { ListRenderer } from "@web/views/list/list_renderer";
import { registry } from "@web/core/registry";
import { X2ManyField } from "@web/views/fields/x2many/x2many_field";


export class One2ManyField extends ListRenderer {
  setup(){
    super.setup()
    console.log("One2ManyField Field Inherited")
}
  get aggregates() {
    const aggregates = {};
    const records = this.props.list.records.map((r) => r.data);
    
    for (const fieldName in this.props.list.activeFields) {
      const field = this.fields[fieldName];
      const values = records
        .map((v) => v[fieldName])
        .filter((v) => v || v === 0);
      
      const func = field.group_operator;

      if (func) {
        let aggregateValue = 0;
        if (func === "max") {
          aggregateValue = Math.max(-Infinity, ...values);
        } else if (func === "min") {
          aggregateValue = Math.min(Infinity, ...values);
        } else if (func === "avg") {
          aggregateValue =
            values.reduce((acc, val) => acc + val) / values.length;
        } else if (func === "sum") {
          aggregateValue = values.reduce((acc, val) => acc + val);
        }

        aggregates[fieldName] = {
          value: aggregateValue,
        };
      }
    }
    return aggregates;
  }
}

One2ManyField.template = "web.ListRenderer";

class One2ManyAggregatorField extends X2ManyField {}

One2ManyAggregatorField.components = { One2ManyField };

One2ManyAggregatorField.template = "owl.One2ManyAggregatorField";
One2ManyAggregatorField.supportedTypes = ["one2many"]

registry.category("fields").add("one2manyAggregator", One2ManyAggregatorField);