MODULE intertest
    VAR string strfnum;
    VAR string script;

    !creating interrupts to allow other robot to controll air and saw
    VAR intnum SuccWon;
    VAR intnum SuccWoff;
    VAR intnum SuccFon;
    VAR intnum SuccFoff;
    VAR intnum SawOnn;
    VAR intnum SawOff;

    PROC main()
        !connecting interrupts with trap functions
        CONNECT SuccWon WITH SuccWonT;
        CONNECT SuccWoff WITH SuccWoffT;
        CONNECT SuccFon WITH SuccFonT;
        CONNECT SuccFoff WITH SuccFoffT;
        CONNECT SawOnn WITH SawOnT;
        CONNECT SawOff WITH SawOffT;
        !linking interrupts to input signals
        ISignalDI SuccW,high,SuccWon;
        ISignalDI SuccW,low,SuccWoff;
        ISignalDI SuccF,high,SuccFon;
        ISignalDI SuccF,low,SuccFoff;
        ISignalDI SawOn,high,SawOnn;
        ISignalDI SawOn,low,Sawoff;
        !resetting signals
        SetDO Wdone,0;
        SetDO Fdone,0;

        !go to home position
        MoveAbsJ [[0.0637,-2.9843,57.4957,-179.9218,54.5115,-90.0454],[5420,9E9,9E9,9E9,9E9,9E9]],v500,fine,tool0;

        !wait to give time to set up picknplace script and reset its signals
        WaitTime 20;
        !load and execute milling scripts
        FOR i FROM 1 TO 13 DO
            strfnum:=NumToStr(i,0);
            script:="HOME:/milling/production_run_1/script"+strfnum+"/script"+strfnum+"_T_ROB1.MOD";
            Load\Dynamic,script;
            IF i MOD 2=1 AND i<8 THEN
                WaitDI Fplaced,1;
                %"script"+strfnum+"_T_ROB1:main"%;
                SetDO Fdone,1;
            ELSE
                WaitDI Wplaced,1;
                %"script"+strfnum+"_T_ROB1:main"%;
                SetDO Wdone,1;
            ENDIF

            UnLoad script;
        ENDFOR
    ENDPROC

    !trap functions for interrupts
    TRAP SuccWonT
        SetDO\Sync,ex600_VALVE_2,1;
        RETURN ;
    ENDTRAP

    TRAP SuccWoffT
        SetDO\Sync,ex600_VALVE_2,0;
        SetDO Wdone,0;
        RETURN ;
    ENDTRAP

    TRAP SuccFonT
        SetDO\Sync,ex600_VALVE_1,1;
        RETURN ;
    ENDTRAP

    TRAP SuccFoffT
        SetDO\Sync,ex600_VALVE_1,0;
        SetDO Fdone,0;
        RETURN ;
    ENDTRAP

    TRAP SawonT
        SetDO EX600_DO_5,1;
    ENDTRAP

    TRAP SawoffT
        SetDO EX600_DO_5,0;
    ENDTRAP
ENDMODULE
