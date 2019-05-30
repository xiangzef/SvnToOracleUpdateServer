create or replace procedure searchversion(v_l_mode in number:=1,
                                          --return_code out number,
                                          return_str  out varchar2,
                                          rs1  out SCV.DS) is
  /**********************************************************
    ��  �ƣ���ȡ�����
    ��  �ܣ�
    ��  �Σ�
    ��  �Σ�return_code    ���ش���
            return_Str     ������Ϣ
            SSV        �������ݼ�
    �����ߣ�xzf
    ��  ����
    ��  �ڣ�2019��5��30��
    ��  ����version beta 0.0.1
  ***********************************************************/
  v_vc_ycbz              varchar2(1);
begin
  v_vc_ycbz := 'Y';
  
  if v_l_mode = 1 then
    for cur in(select row_number() over(partition by  substr(t.edition,5,8) order by t.tversion desc ) rn,t.rowid
                 from tupdate t   
                where lengthb(t.edition)<15 
                and substr(t.edition,5,6)<>'160620')loop
    update tupdate t  set rn = cur.rn 
           where t.rowid = cur.rowid;
    end loop;
    commit;
  end if;
  
  
  open rs1 for
  select t.* from tupdate t  where t.rn = 1;
  v_vc_ycbz := 'N';
  
  --return_code := 0;
  --return_str := 'searchversion';
exception when others then
  --ϵͳ�Զ��쳣��׽
  if v_vc_ycbz = 'N' then
    --return_code:=-1;
    return_str := '[searchversion]���쳣����:'||chr(13)||sqlerrm;
  end if;
  --��Ϊ����ϵͳ�쳣
  if v_vc_ycbz = 'Y' then
    return_str := return_str||chr(13)||sqlerrm;
  end if;
end searchversion;
/
