import enum
import hashlib
import random
from datetime import datetime

from flask_login import UserMixin
from sqlalchemy import Column, Integer, String, Float, ForeignKey, Enum, DateTime, Boolean, BOOLEAN, DATETIME
from sqlalchemy.orm import relationship

from app import db, app


class UserRole(enum.Enum):
    NHAN_VIEN = 1
    QUAN_LY = 2


class QuyDinhEnum(enum.Enum):
    SO_KHACH_TOI_DA_TRONG_PHONG = "so_khach_toi_da_trong_phong"
    SO_LUONG_KHACH_PHU_THU = "so_luong_khach_phu_thu"
    TY_LE_PHU_THU = "ty_le_phu_thu"


class User(db.Model, UserMixin):
    id = Column(Integer, primary_key=True, nullable=False, autoincrement=True)
    username = Column(String(45), unique=True, nullable=True)
    password = Column(String(45), nullable=True)
    ten = Column(String(45), nullable=False)
    ho = Column(String(22), nullable=False)
    gioi_tinh = Column(BOOLEAN, nullable=False, default=False)
    ngay_sinh = Column(DATETIME, nullable=True)
    cccd = Column(String(15), nullable=False, unique=True)
    user_role = Column(Enum(UserRole), default=UserRole.QUAN_LY)


class LoaiPhongEnum(enum.Enum):
    VIP = 1
    THUONG = 2
    SIEUVIP = 3


class TinhTrangPhongEnum(enum.Enum):
    TRONG = 1
    DA_DAT = 2
    DANG_O = 3


class KhachHangEnum(enum.Enum):
    NOI_DIA = 1
    NUOC_NGOAI = 2


class KhachHang(db.Model):
    id = Column(Integer, primary_key=True, autoincrement=True)
    ten_khach_hang = Column(String(30), nullable=False)
    loai_khach_hang = Column(Enum(KhachHangEnum), nullable=False)
    cmnd = Column(Integer, nullable=False)
    dia_chi = Column(String(50), nullable=False)
    id_chi_tiet_dat_phong = Column(Integer, ForeignKey('chi_tiet_dat_phong.id'), nullable=False)


class ChiTietDatPhong(db.Model):
    id = Column(Integer, primary_key=True, autoincrement=True)

    id_phieu_dat_phong = Column(Integer, ForeignKey('phieu_dat_phong.id'))
    id_phong = Column(Integer, ForeignKey('phong.id'))

    don_gia = Column(Integer, nullable=False)
    phong = relationship('Phong')
    phieu_dat_phong = relationship('PhieuDatPhong', back_populates='cac_chi_tiet_dat_phong')
    cac_khach_hang = relationship('KhachHang')


class Phong(db.Model):
    id = Column(Integer, primary_key=True, autoincrement=True)
    ma_phong = Column(String(10), nullable=False)
    loai_phong = Column(Enum(LoaiPhongEnum), nullable=False)
    don_gia = Column(Integer, nullable=False)
    tinh_trang = Column(Enum(TinhTrangPhongEnum), nullable=False)


class PhieuDatPhong(db.Model):
    id = Column(Integer, primary_key=True, autoincrement=True)
    ten_nguoi_dat = Column(String(30), nullable=False)
    ngay_dat_phong = Column(DateTime, nullable=False)
    ngay_tra_phong = Column(DateTime, nullable=False)
    cac_chi_tiet_dat_phong = relationship('ChiTietDatPhong', back_populates='phieu_dat_phong')


class PhieuThuePhong(db.Model):
    id = Column(Integer, primary_key=True, autoincrement=True)
    id_phieu_dat_phong = Column(Integer, ForeignKey('phieu_dat_phong.id'), unique=True)
    phieu_dat_phong = relationship('PhieuDatPhong')


class QuyDinh(db.Model):
    key = Column(Enum(QuyDinhEnum), primary_key=True)
    value = Column(Integer, nullable=False)


if __name__ == '__main__':
    with app.app_context():
        db.drop_all()
        db.create_all()

        # Thêm 5 bản ghi mẫu cho model Phong
        for _ in range(5):
            phong = Phong(
                ma_phong=f"Phong{_}",
                loai_phong=random.choice(list(LoaiPhongEnum)),
                don_gia=1000000 + _ * 100000,
                tinh_trang=TinhTrangPhongEnum.TRONG
            )
            db.session.add(phong)
        db.session.commit()

        # Thêm 5 bản ghi mẫu cho model PhieuDatPhong

        phieu_dat_phong1 = PhieuDatPhong(
            ten_nguoi_dat=f"NguoiDat{1}",
            ngay_dat_phong=datetime.now(),
            ngay_tra_phong=datetime(year=2024, month=1, day=16)
        )
        db.session.add(phieu_dat_phong1)
        phieu_dat_phong2 = PhieuDatPhong(
            ten_nguoi_dat=f"NguoiDat{2}",
            ngay_dat_phong=datetime.now(),
            ngay_tra_phong=datetime(year=2024, month=1, day=18)
        )
        db.session.add(phieu_dat_phong2)
        phieu_dat_phong3 = PhieuDatPhong(
            ten_nguoi_dat=f"NguoiDat{3}",
            ngay_dat_phong=datetime.now(),
            ngay_tra_phong=datetime(year=2024, month=1, day=20)
        )
        db.session.add(phieu_dat_phong3)
        phieu_dat_phong4 = PhieuDatPhong(
            ten_nguoi_dat=f"NguoiDat{4}",
            ngay_dat_phong=datetime.now(),
            ngay_tra_phong=datetime(year=2024, month=1, day=25)
        )
        db.session.add(phieu_dat_phong4)
        phieu_dat_phong5 = PhieuDatPhong(
            ten_nguoi_dat=f"NguoiDat{5}",
            ngay_dat_phong=datetime.now(),
            ngay_tra_phong=datetime(year=2024, month=1, day=30)
        )
        db.session.add(phieu_dat_phong5)
        db.session.commit()

        # Thêm 5 bản ghi mẫu cho model ChiTietDatPhong
        for _ in range(5):
            chi_tiet_dat_phong = ChiTietDatPhong(
                id_phong=_ + 1,  # Giả sử idPhong tăng dần từ 1
                id_phieu_dat_phong=_ + 1,  # Giả sử idPhieuDatPhong tăng dần từ 1
                don_gia=1000000 + _ * 100000
            )
            db.session.add(chi_tiet_dat_phong)
        db.session.commit()

        for _ in range(5):
            khach_hang = KhachHang(
                ten_khach_hang=f"KhachHang{_}",
                loai_khach_hang=KhachHangEnum.NOI_DIA,
                cmnd=1000000000 + _,
                dia_chi=f"DiaChi{_}",
                id_chi_tiet_dat_phong=_ + 1  # Giả sử mã đặt phòng tăng dần từ 1
            )
            db.session.add(khach_hang)
        db.session.commit()

        # Thêm 5 bản ghi mẫu cho model PhieuThuePhong
        for _ in range(5):
            phieu_thue_phong = PhieuThuePhong(
                id_phieu_dat_phong=_ + 1  # Giả sử idDatPhong tăng dần từ 1
            )
            db.session.add(phieu_thue_phong)

        # Lưu các thay đổi vào cơ sở dữ liệu
        db.session.commit()

        admin = User(username='admin', password=hashlib.md5('123'.encode('utf-8')).hexdigest(), ten='admin', ho='admin',
                     gioi_tinh=True, cccd="123", user_role=UserRole.QUAN_LY)
        nv = User(username='nv', password=hashlib.md5('123'.encode('utf-8')).hexdigest(), ten='admin', ho='admin',
                  gioi_tinh=True, cccd="12333", user_role=UserRole.NHAN_VIEN)

        db.session.add(nv)
        db.session.add(admin)
        db.session.commit()
