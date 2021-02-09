import json

from sepal_ui import sepalwidgets as sw 
import ipyvuetify as v

from component.message import cm
from component import parameter as cp
from component import widget as cw
from component import scripts as cs

class accc_process(sw.Tile):

    def __init__(self, io):
        
        # gather io 
        self.io = io 
        
        # create the widgets
        connectivity = v.Select(
            label = cm.acc.connectivity,
            items = cp.connectivity,
            v_model = cp.connectivity[0]
        )
        res = v.TextField(
            label = cm.acc.res,
            type= 'number',
            v_model = None
        )
        thresholds = cw.Thresholds(label = cm.acc.thresholds)
        options = v.Select(
            label = cm.acc.options,
            items= cp.options,
            v_model = cp.options[0]['value']
        )
        
        
        # bind to the io
        self.output = sw.Alert() \
            .bind(connectivity, self.io, 'connectivity') \
            .bind(res, self.io, 'res') \
            .bind(thresholds.save, self.io, 'thresholds') \
            .bind(options, self.io, 'options')
        
        # create the btn 
        btn = sw.Btn('Start acc process')
        
        super().__init__(
            self.io.tile_id,
            "Run Process",
            inputs = [
                connectivity,
                res,
                thresholds,
                options
            ],
            output = self.output,
            btn = btn
        )
        
        # link js behaviours
        btn.on_event('click', self._on_click)
        
    def _on_click(self, widget, event, data):
        
        # silence the btn
        widget.toggle_loading()
        
        # check inputs 
        if not self.output.check_input(self.io.connectivity, cm.acc.no_connex): return widget.toggle_loading()
        if not self.output.check_input(self.io.res, cm.acc.no_res): return widget.toggle_loading()
        if not self.output.check_input(len(json.loads(self.io.thresholds)) or None, cm.acc.no_thres): return widget.toggle_loading()
        if not self.output.check_input(self.io.option, cm.acc.no_options): return widget.toggle_loading()
        if not self.output.check_input(self.io.bin_map, cm.bin.no_bin): return widget.toggle_loading()
        
        try:
            
            # update the params list 
            self.io.update_params_list()
        
            # compute acc process 
            txt, tif, csv = cs.run_gwb_process(
                self.io.process, 
                self.io.bin_map, 
                self.io.params_list, 
                self.io.get_params_list, 
                self.output
            )
            
            # add the files to the download links
            
        except Exception as e:
            self.output.add_live_msg(str(e), 'error')
            
        # release the btn 
        widget.toggle_loading()
        
        return