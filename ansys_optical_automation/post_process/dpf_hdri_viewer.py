import csv
import math
import os
import time

from ansys_optical_automation.post_process.dpf_base import DataProcessingFramework


class DpfHdriViewer(DataProcessingFramework):
    """
    Provides for launching Speos postprocessing software, Virtual reality lab.

    This framework is used to interact with the software and automatically perform
    analysis and postprocessing on the simulation results
    """

    def __init__(self):
        """Initialize DPF as HDRIViewer."""
        DataProcessingFramework.__init__(
            self, extension=(".speos360", ".optisvr", ".xmp"), application="HDRIViewer.Application"
        )
        self.source_list = []

    def get_source_list(self):
        """
        Get the source list stored in the simulation result.

        Returns
        -------
        list
            List of sources available in the postprocessing file.
        """
        self.source_list = []
        if self.dpf_instance is not None:
            total_sources = self.dpf_instance.GetNbSources
            for layer in range(total_sources):
                self.source_list.append(self.dpf_instance.GetSourceName(layer))
            return self.source_list
        else:
            raise ImportError("Object is not a valid SpeosVRObject.")

    def __export_vr_view(self, export_path, phi_angles=None, theta_angles=None):
        """
        Export VR results for defined angles or all angles as image (JPG) files.

        Parameters
        ----------
        export_path : string
            Path for exporting the set of JPG files. If this path does not exist,
            it is created.
        phi_angles : list of floats, optional
            List of phi angles to export. The default is ``None``, in which case
            all phi angles are exported.
        theta_angles : list of floats, optional
            List of theta angles to export. The default is ``None``, in which case
            all theta angles are exported.
        """
        if phi_angles is None and theta_angles is None:
            "Export all angle combinations"
            self.dpf_instance.Show(True)
            self.dpf_instance.ExportAllObserverImages(export_path + "\\", 0)
        else:
            "Export angle combinations provided"
            for count in range(len(phi_angles)):
                try:
                    self.dpf_instance.SetSightDirection(phi_angles[count], theta_angles[count])
                    self.dpf_instance.Show(True)
                    self.dpf_instance.ExportObserverImage(
                        export_path
                        + r"\image"
                        + str(math.degrees([phi_angles[count]]))
                        + str(math.degrees([theta_angles[count]]))
                        + ".JPG"
                    )
                except Exception as e:
                    raise TypeError(
                        str(phi_angles) + str(theta_angles) + " are not existing iin the file \n Details: " + e
                    )

    def export_vr_views(self, export_path=None, phi_angles=None, theta_angles=None, config_ids=None):
        """
        Export VR results for all or specific configurations for defined angles or all angles as image (JPG) files.

        Parameters
        ----------
        export_path : string
            Path for exporting the JPG files. If this path does not exist,
            it is created.
        phi_angles : list of floats, optional
            List of phi angles to export. The default is ``None``, in which case
            all phi angles are exported.
        theta_angles : list of floats, optional
            List of theta angles to export. The default is ``None``, in which case
            all theta angles are exported.
        config_ids : list of positive integers or list of strings or a string or an integer, optional
            List of configurations IDs to export. The default is ``None``, in which case all configuration
            IDs are exported.
        """
        if export_path is None:
            export_path = os.path.dirname(self.file_path)

        if config_ids is None:
            "Export all configurations"
            config_ids = self.dpf_instance.GetNbConfigurations
            for config in range(config_ids):
                self.dpf_instance.SetConfigurationById(config)
                self.valid_dir(os.path.join(export_path, str(config)))
                self.__export_vr_view(os.path.join(export_path, str(config)), phi_angles, theta_angles)

        elif isinstance(config_ids, int):
            try:
                self.dpf_instance.SetConfigurationById(config_ids)
                self.valid_dir(os.path.join(export_path, str(config_ids)))
                self.__export_vr_view(os.path.join(export_path, str(config_ids)), phi_angles, theta_angles)
            except Exception as e:
                raise ValueError(str(config_ids) + " a non valid ID exists in the file \n Details: " + e)

        elif isinstance(config_ids, str):
            try:
                self.dpf_instance.SetConfigurationByName(config_ids)
                self.valid_dir(os.path.join(export_path, str(config_ids)))
                self.__export_vr_view(os.path.join(export_path, str(config_ids)), phi_angles, theta_angles)
            except Exception as e:
                raise ValueError(config_ids + " does not exist in the file \n Details: " + e)

        elif isinstance(config_ids, list):
            for item in config_ids:
                self.valid_dir(os.path.join(export_path, str(item)))
                if isinstance(config_ids[0], int):
                    try:
                        self.dpf_instance.SetConfigurationById(item)
                        self.__export_vr_view(os.path.join(export_path, str(item)), phi_angles, theta_angles)
                    except Exception as e:
                        raise ValueError(str(item) + " a non valid ID exists in the file \n Details: " + e)
                else:
                    try:
                        self.dpf_instance.SetConfigurationByName(item)
                        self.__export_vr_view(os.path.join(export_path, str(item)), phi_angles, theta_angles)
                    except Exception as e:
                        raise ValueError(item + " does not exist in the file \n Details: " + e)

    def set_source_power(self, source, value):
        """
        Set the source with power value provided.

        Parameters
        ----------
        source : int/str
            source defined by id or name.
        value : float
            source power.

        Returns
        -------


        """
        if len(self.source_list) == 0:
            self.source_list = self.get_source_list()
        if isinstance(source, int):
            if source >= len(self.source_list):
                msg = "source requested does not exist"
                raise ValueError(msg)
            self.dpf_instance.SetSourcePowerById(source, value)
        else:
            if source not in self.source_list:
                msg = "source requested does not exist"
                raise ValueError(msg)
            self.dpf_instance.SetSourcePowerByName(source, value)

    def set_source_ratio(self, source, value):
        """
        Set the source with power ratio value provided.

        Parameters
        ----------
        source : int/str
            source defined by id or name
        value : float
            source power ratio

        Returns
        -------


        """
        if len(self.source_list) == 0:
            self.source_list = self.get_source_list()
        if isinstance(source, int):
            if source >= len(self.source_list):
                msg = "source requested does not exist"
                raise ValueError(msg)
            self.dpf_instance.SetSourceRatioById(source, value)
        else:
            if source not in self.source_list:
                msg = "source requested does not exist"
                raise ValueError(msg)
            self.dpf_instance.SetSourceRatioByName(source, value)

    def timeline_animation_run(self, csv_file):
        """
        function to run animation in observer result.

        Parameters
        ----------
        csv_file : str
            file path of time line csv file

        Returns
        -------


        """
        source_list = self.source_list if len(self.source_list) != 0 else self.get_source_list()
        csv_source_list = []
        csv_source_animation = []
        with open(csv_file) as file:
            content = csv.reader(file, delimiter=",")
            First_Row = True
            for row in content:
                if First_Row:
                    csv_source_list = [item for item in row][1:]
                else:
                    csv_source_animation.append([float(item) for item in row])
                First_Row = False
        animation_time_step = csv_source_animation[1][0] - csv_source_animation[0][0]
        if len(csv_source_list) != len(source_list):
            msg = "selected timeline csv file does not match with the speos vr file"
            raise ImportError(msg)

        if set(csv_source_list) != set(source_list):
            print("will assume source using index")
            self.dpf_instance.Show(1)
            while True:
                for csv_source_config in csv_source_animation:
                    for source_idx, source in enumerate(csv_source_list):
                        self.set_source_power(source_idx, csv_source_config[source_idx + 1])
                    time.sleep(animation_time_step)
        else:
            print("will use name to set source in animation")
            self.dpf_instance.Show(1)
            while True:
                for csv_source_config in csv_source_animation:
                    for source_idx, source in enumerate(csv_source_list):
                        self.set_source_power(source, csv_source_config[source_idx + 1])
                    time.sleep(animation_time_step)
