from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relationship

from ...BaseSQLAlchemy import Base

class GPUOutputsData(Base):
    __tablename__ = 'pcpartpicker_gpu_outputs_data'

    id = Column(Integer, primary_key=True, autoincrement=True)
    # Output columns
    hdmi_outputs = Column(Integer, default=None)
    displayport_outputs = Column(Integer, default=None)
    hdmi_2_1a_outputs = Column(Integer, default=None)
    displayport_1_4_outputs = Column(Integer, default=None)
    displayport_1_4a_outputs = Column(Integer, default=None)
    dvi_d_dual_link_outputs = Column(Integer, default=None)
    hdmi_2_1_outputs = Column(Integer, default=None)
    displayport_2_1_outputs = Column(Integer, default=None)
    displayport_2_0_outputs = Column(Integer, default=None)
    hdmi_2_0b_outputs = Column(Integer, default=None)
    dvi_i_dual_link_outputs = Column(Integer, default=None)
    usb_type_c_outputs = Column(Integer, default=None)
    vga_outputs = Column(Integer, default=None)
    virtuallink_outputs = Column(Integer, default=None)
    dvi_d_single_link_outputs = Column(Integer, default=None)
    minidisplayport_2_1_outputs = Column(Integer, default=None)
    hdmi_2_0_outputs = Column(Integer, default=None)
    dvi_outputs = Column(Integer, default=None)
    minidisplayport_outputs = Column(Integer, default=None)
    hdmi_1_4_outputs = Column(Integer, default=None)
    minidisplayport_1_4a_outputs = Column(Integer, default=None)
    minidisplayport_1_4_outputs = Column(Integer, default=None)
    vhdci_outputs = Column(Integer, default=None)
    dvi_i_single_link_outputs = Column(Integer, default=None)
    s_video_outputs = Column(Integer, default=None)
    mini_hdmi_outputs = Column(Integer, default=None)
    displayport_1_3_outputs = Column(Integer, default=None)
    dvi_a_outputs = Column(Integer, default=None)

    gpu_id = Column(Integer, ForeignKey('pcpartpicker_gpu_main_data.id'), unique=True, nullable=False)
    gpu = relationship("GPUMainData")